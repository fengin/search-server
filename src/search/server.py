#描述：基于即梦AI的图像生成服务，专门设计用于与Cursor IDE集成。它接收来自Cursor的文本描述，生成相应的图像，并提供图片下载和保存功能。
#作者：凌封 (微信fengin)
#GITHUB: https://github.com/fengin/search-server.git
#相关知识可以看AI全书：https://aibook.ren 


from typing import Any, Dict, List, Optional
import asyncio
import os
import time
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from sys import stdin, stdout

# mcp核心协议源码对unicode编码处理还有bug，需手动指定为utf-8
stdin.reconfigure(encoding='utf-8')
stdout.reconfigure(encoding='utf-8')

# 检查API密钥
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    BRAVE_API_KEY = "BSAjHuch7***daGe8x1kpI***d-Wemk0"

if not BRAVE_API_KEY:
    raise ValueError("需要设置BRAVE_API_KEY环境变量")

# 速率限制配置
RATE_LIMIT = {
    "per_second": 1,
    "per_month": 15000
}

request_count = {
    "second": 0,
    "month": 0,
    "last_reset": time.time()
}

def check_rate_limit():
    """检查并更新速率限制"""
    now = time.time()
    if now - request_count["last_reset"] > 1:
        request_count["second"] = 0
        request_count["last_reset"] = now
    
    if (request_count["second"] >= RATE_LIMIT["per_second"] or 
        request_count["month"] >= RATE_LIMIT["per_month"]):
        raise Exception("超出速率限制")
    
    request_count["second"] += 1
    request_count["month"] += 1

server = Server("search")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用的搜索工具"""
    return [
        types.Tool(
            name="web_search",
            description=(
                "使用Brave搜索API执行网络搜索，适用于一般查询、新闻、文章和在线内容。"
                "适合广泛的信息收集、近期事件，或需要多样化网络来源时使用。"
                "支持分页、内容过滤和时效性控制。"
                "每次请求最多返回20个结果，支持分页偏移。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询(最多400字符，50个词)"
                    },
                    "count": {
                        "type": "number",
                        "description": "结果数量(1-20，默认10)",
                        "default": 10
                    },
                    "offset": {
                        "type": "number", 
                        "description": "分页偏移量(最大9，默认0)",
                        "default": 0
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="local_search",
            description=(
                "使用Brave本地搜索API搜索商家和地点。"
                "最适合与实体位置、商家、餐厅、服务等相关的查询。"
                "返回详细信息包括:\n"
                "- 商家名称和地址\n"
                "- 评分和评论数\n"
                "- 电话号码和营业时间\n"
                "适用于查询包含‘附近’或提到特定位置的场景，"
                "如果没有找到本地结果会自动回退到网络搜索。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "本地搜索查询(例如:'中央公园附近的披萨')"
                    },
                    "count": {
                        "type": "number",
                        "description": "结果数量(1-20，默认5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    ]

async def perform_web_search(query: str, count: int = 10, offset: int = 0) -> str:
    """执行网络搜索"""
    check_rate_limit()
    url = "https://api.search.brave.com/res/v1/web/search"
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_API_KEY
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Brave API错误: {response.status_code} {response.text}")
            
        data = response.json()
        results = []
        for result in data.get("web", {}).get("results", []):
            results.append(
                f"标题: {result.get('title', '')}\n"
                f"描述: {result.get('description', '')}\n"
                f"网址: {result.get('url', '')}"
            )
            
        return "\n\n".join(results)

async def perform_local_search(query: str, count: int = 5) -> str:
    """执行本地搜索"""
    check_rate_limit()
    
    # 初始搜索获取位置ID
    web_url = "https://api.search.brave.com/res/v1/web/search"
    params = {
        "q": query,
        "search_lang": "en",
        "result_filter": "locations",
        "count": min(count, 20)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            web_url,
            params=params,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_API_KEY
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Brave API错误: {response.status_code} {response.text}")
            
        data = response.json()
        location_ids = [
            r["id"] for r in data.get("locations", {}).get("results", [])
            if "id" in r
        ]
        
        if not location_ids:
            return await perform_web_search(query, count)
            
        # 并行获取POI详情和描述
        pois_url = "https://api.search.brave.com/res/v1/local/pois"
        desc_url = "https://api.search.brave.com/res/v1/local/descriptions"
        
        pois_response = await client.get(
            pois_url,
            params={"ids": location_ids},
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_API_KEY
            }
        )
        
        desc_response = await client.get(
            desc_url,
            params={"ids": location_ids},
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_API_KEY
            }
        )
        
        if pois_response.status_code != 200 or desc_response.status_code != 200:
            raise Exception("获取POI详情或描述失败")
            
        pois_data = pois_response.json()
        desc_data = desc_response.json()
        
        results = []
        for poi in pois_data.get("results", []):
            address_parts = [
                poi.get("address", {}).get("streetAddress", ""),
                poi.get("address", {}).get("addressLocality", ""),
                poi.get("address", {}).get("addressRegion", ""),
                poi.get("address", {}).get("postalCode", "")
            ]
            address = ", ".join(filter(None, address_parts)) or "暂无"
            
            rating = poi.get("rating", {})
            description = desc_data.get("descriptions", {}).get(poi["id"], "暂无描述")
            
            results.append(
                f"名称: {poi.get('name', '暂无')}\n"
                f"地址: {address}\n"
                f"电话: {poi.get('phone', '暂无')}\n"
                f"评分: {rating.get('ratingValue', '暂无')} ({rating.get('ratingCount', 0)}条评论)\n"
                f"价格范围: {poi.get('priceRange', '暂无')}\n"
                f"营业时间: {', '.join(poi.get('openingHours', [])) or '暂无'}\n"
                f"描述: {description}"
            )
            
        return "\n---\n".join(results) if results else "未找到本地结果"

@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: Optional[Dict[str, Any]]
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用请求"""
    try:
        if not arguments:
            raise ValueError("缺少参数")
            
        if name == "web_search":
            query = arguments.get("query")
            count = arguments.get("count", 10)
            offset = arguments.get("offset", 0)
            
            if not query:
                raise ValueError("缺少query参数")
                
            results = await perform_web_search(query, count, offset)
            return [types.TextContent(type="text", text=results)]
            
        elif name == "local_search":
            query = arguments.get("query")
            count = arguments.get("count", 5)
            
            if not query:
                raise ValueError("缺少query参数")
                
            results = await perform_local_search(query, count)
            return [types.TextContent(type="text", text=results)]
            
        else:
            raise ValueError(f"未知工具: {name}")
            
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"错误: {str(e)}"
        )]

async def main():
    # 使用标准输入/输出流运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="search",
                server_version="0.0.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# 如果你想连接到自定义客户端，这是必需的
if __name__ == "__main__":
    asyncio.run(main())