"""
秘塔AI客户端

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

from typing import AsyncGenerator, Optional, Dict, Any, List
from playwright.async_api import async_playwright, Page, CDPSession, Browser, BrowserContext
import asyncio
import json
import time
import re
from .constants import *
from .exceptions import *
from .response_handler import MetasoResponseHandler

class MetasoClient:
    """秘塔AI客户端"""
    
    def __init__(self, uid: str, sid: str, browser_data_dir: str = "tmp/browser"):
        """初始化客户端
        
        Args:
            uid: 用户ID
            sid: 会话ID
            browser_data_dir: 浏览器数据目录，默认为 "tmp/browser"
        """
        self._uid = uid
        self._sid = sid
        self._browser_data_dir = browser_data_dir
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._client: Optional[CDPSession] = None
        self._meta_token: Optional[str] = None
        self._response_handler = MetasoResponseHandler()
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._init_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
        
    async def close(self):
        """关闭客户端"""
        try:
            if self._client:
                await self._client.detach()
                self._client = None
            if self._page:
                await self._page.close()
                self._page = None
            if self._context:
                await self._context.close()
                self._context = None
            if self._browser:
                await self._browser.close()
                self._browser = None
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
    async def _init_browser(self):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self._context = await playwright.chromium.launch_persistent_context(
            self._browser_data_dir,
            headless=True,
            ignore_https_errors=True,
            user_agent=FAKE_HEADERS["User-Agent"],
            viewport=None,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--hide-scrollbars",
                "--mute-audio",
                "--disable-gpu",
                "--disable-web-security",
                "--process-per-tab"
            ]
        )
        self._page = await self._context.new_page()
        
        # 隐藏webdriver特征
        await self._page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            window.navigator.chrome = {
                runtime: {}
            };
            delete navigator.__proto__.webdriver;
        """)
        
        # 设置User-Agent
        await self._page.set_extra_http_headers(FAKE_HEADERS)
        
        # 设置cookies
        await self._context.add_cookies([
            {
                "name": "uid", 
                "value": self._uid,
                "url": "https://metaso.cn"
            },
            {
                "name": "sid", 
                "value": self._sid,
                "url": "https://metaso.cn"
            }
        ])
        
        # 创建CDP会话
        self._client = await self._page.context.new_cdp_session(self._page)
        await self._client.send("Fetch.enable", {
            "patterns": [{
                "urlPattern": "https://metaso.cn/api/searchV2*",
                "requestStage": "Response"
            }]
        })
        
        # 获取初始meta token
        self._meta_token = await self._get_meta_token()

    async def _get_meta_token(self) -> str:
        """获取meta token
        
        Returns:
            str: meta token
        """
        if self._meta_token:
            return self._meta_token
            
        # 导航到首页
        await self._page.goto(BASE_URL)
        
        # 等待meta-token元素加载，不要求可见
        meta_token_element = await self._page.wait_for_selector('meta#meta-token', state='attached')
        if not meta_token_element:
            raise MetasoException(*API_REQUEST_FAILED)
            
        # 获取content属性
        meta_token = await meta_token_element.get_attribute('content')
        if not meta_token:
            raise MetasoException(*API_REQUEST_FAILED)
            
        return meta_token
        
    async def _create_conversation(self, content: str, model: str = DEFAULT_MODEL) -> str:
        """创建会话
        
        Args:
            content: 对话内容
            model: 模型名称,默认为detail
            
        Returns:
            str: 会话ID
        """
        headers = {
            **FAKE_HEADERS,
            'Content-Type': 'application/json',
            'Token': self._meta_token,
            'Is-Mini-Webview': '0',
            'Cookie': f'uid={self._uid}; sid={self._sid}',
            'Origin': 'https://metaso.cn',
            'Referer': 'https://metaso.cn/',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
        }
        
        data = {
            "question": content,
            "mode": model,
            "engineType": "",
            "scholarSearchDomain": "all"
        }
        
        # 发送请求
        js_code = """
            async (args) => {
                try {
                    console.log('Sending request with args:', JSON.stringify(args));
                    const response = await fetch(args.url, {
                        method: 'POST',
                        headers: args.headers,
                        body: JSON.stringify(args.data),
                        credentials: 'include'
                    });
                    
                    console.log('Response status:', response.status);
                    if (!response.ok) {
                        console.error('Response not ok:', response.status);
                        return null;
                    }
                    
                    const result = await response.json();
                    console.log('Response:', JSON.stringify(result));
                    
                    if (result.errCode) {
                        console.error('Error code:', result.errCode, result.errMsg);
                        return null;
                    }
                    
                    return result;
                } catch (error) {
                    console.error('Error:', error);
                    return null;
                }
            }
        """
        
        args = {
            "url": API_SESSION_URL,
            "headers": headers,
            "data": data
        }
        
        response = await self._page.evaluate(js_code, args)
        
        # 检查响应
        if not response:
            raise MetasoException(*API_REQUEST_FAILED)
            
        if 'data' not in response or 'id' not in response['data']:
            print(f"Response missing id: {response}")
            raise MetasoException(*API_REQUEST_FAILED)
            
        return response['data']['id']
        
    async def get_completion(self, content: str, model: str = DEFAULT_MODEL) -> Dict:
        """非流式对话
        
        Args:
            content: 对话内容
            model: 使用的模型名称
            
        Returns:
            Dict: 包含处理后的完整响应
        """
        try:
            # 创建新的响应处理器实例
            self._response_handler = MetasoResponseHandler()
            
            # 创建会话
            conv_id = await self._create_conversation(content, model)
            
            # 构造搜索URL
            search_url = f"{BASE_URL}/search/{conv_id}?q={content}"
            
            # 创建队列和事件
            queue = asyncio.Queue()
            response_event = asyncio.Event()
            
            # 定义元信息
            meta_info = {
                "model": model,
                "conversation_id": conv_id,
                "query": content,
                "timestamp": int(time.time())
            }
            
            async def handle_response(event):
                try:
                    request_id = event["requestId"]
                    
                    # 获取响应流
                    stream_result = await self._client.send("Fetch.takeResponseBodyAsStream", {"requestId": request_id})
                    stream_handle = stream_result["stream"]
                    if not stream_handle:
                        return
                        
                    try:
                        buffer = ""
                        while True:
                            read_result = await self._client.send("IO.read", {"handle": stream_handle, "size": 256})
                            if not read_result:
                                break
                                
                            data = read_result.get("data")
                            eof = read_result.get("eof")
                            
                            if data:
                                buffer += data
                                # 按data:分割处理
                                parts = buffer.split("data:")
                                # 处理完整的部分
                                for part in parts[:-1]:
                                    if part.strip():
                                        cleaned = self._response_handler.clean_response(f"data:{part}")
                                        if cleaned:
                                            await queue.put(cleaned)
                                # 保留最后一个可能不完整的部分        
                                buffer = "data:" + parts[-1] if parts else ""
                            
                            if eof:
                                # 处理剩余数据
                                if buffer.strip():
                                    cleaned = self._response_handler.clean_response(buffer)
                                    if cleaned:
                                        await queue.put(cleaned)
                                break
                                
                    except Exception as e:
                        print(f"Error reading stream: {e}")
                    finally:
                        await self._client.send("IO.close", {"handle": stream_handle})
                        response_event.set()
                    
                except Exception as e:
                    print(f"Error processing response: {e}")
                    response_event.set()
                    
            # 监听响应
            self._client.on("Fetch.requestPaused", handle_response)
            
            try:
                # 导航到搜索页面
                await self._page.goto(search_url)
                # 等待响应完成
                await asyncio.wait_for(response_event.wait(), timeout=30)
                
            finally:
                # 移除监听器
                self._client.remove_listener("Fetch.requestPaused", handle_response)
                
            # 构建返回结果
            result = {
                "content": self._response_handler.content,
                "references": self._response_handler.references,
                "images": self._response_handler.images,
                "tables": self._response_handler.tables,
                "recommended_questions": self._response_handler.recommended_questions,
                "highlights": self._response_handler.highlights,
                "query_info": self._response_handler.query_info,
                "markdown": self._response_handler.format_markdown({}),
                "meta": meta_info
            }
            
            return result
            
        except Exception as e:
            print(f"Error in get_completion: {e}")
            raise MetasoException(*API_REQUEST_FAILED)
        
    async def get_completion_stream(self, content: str, model: str = DEFAULT_MODEL) -> AsyncGenerator[str, None]:
        """获取流式补全
        
        Args:
            content: 对话内容 
            model: 模型名称,默认为detail
            
        Yields:
            str: 清理后的补全内容片段
        """
        try:
            # 创建会话
            conv_id = await self._create_conversation(content, model)
            
            # 构造搜索URL
            search_url = f"{BASE_URL}/search/{conv_id}?q={content}"
            
            # 创建队列用于存储响应片段
            queue = asyncio.Queue()
            response_event = asyncio.Event()
            
            async def handle_response(event):
                try:
                    request_id = event["requestId"]
                    
                    # 获取响应流
                    stream_result = await self._client.send("Fetch.takeResponseBodyAsStream", {"requestId": request_id})
                    stream_handle = stream_result["stream"]
                    if not stream_handle:
                        return
                        
                    try:
                        buffer = ""
                        while True:
                            read_result = await self._client.send("IO.read", {"handle": stream_handle, "size": 256})
                            if not read_result:
                                break
                                
                            data = read_result.get("data")
                            eof = read_result.get("eof")
                            
                            if data:
                                buffer += data
                                # 按data:分割处理
                                parts = buffer.split("data:")
                                # 处理完整的部分
                                for part in parts[:-1]:
                                    if part.strip():
                                        cleaned = self._response_handler.clean_response(f"data:{part}")
                                        if cleaned:
                                            await queue.put(cleaned)
                                # 保留最后一个可能不完整的部分        
                                buffer = "data:" + parts[-1] if parts else ""
                            
                            if eof:
                                # 处理剩余数据
                                if buffer.strip():
                                    cleaned = self._response_handler.clean_response(buffer)
                                    if cleaned:
                                        await queue.put(cleaned)
                                break
                                
                    except Exception as e:
                        print(f"Error reading stream: {e}")
                    finally:
                        # 关闭流
                        await self._client.send("IO.close", {"handle": stream_handle})
                        response_event.set()
                    
                except Exception as e:
                    print(f"Error processing response: {e}")
                    response_event.set()
                    
            # 监听响应
            self._client.on("Fetch.requestPaused", handle_response)
            
            try:
                # 导航到搜索页面
                await self._page.goto(search_url)
                
                # 持续获取响应片段
                while True:
                    try:
                        chunk = await asyncio.wait_for(queue.get(), timeout=1.0)
                        if chunk:  # 只返回非空内容
                            yield chunk
                    except asyncio.TimeoutError:
                        # 检查是否完成
                        if response_event.is_set():
                            break
                            
            finally:
                # 移除监听器
                self._client.remove_listener("Fetch.requestPaused", handle_response)
                    
        except Exception as e:
            print(f"Error in get_completion_stream: {e}")
            raise MetasoException(*API_REQUEST_FAILED)