"""Metaso Search API implementation for MCP server

This module provides web search and academic search functionality using Metaso Search API.
It includes both the API implementation and tool descriptions.
"""

from typing import Dict, Any
import mcp.types as types
import warnings
import sys
from pathlib import Path
import os
import time
from .metaso.client import MetasoClient

# 认证信息
# METASO_UID = os.getenv("METASO_UID")
METASO_UID = "67b0341c6ea19779a9be263f"
# METASO_SID = os.getenv("METASO_SID")
METASO_SID = "b8fb1b5a22ac4347b95e5306aae5a44d"

if not METASO_UID or not METASO_SID:
    raise ValueError("需要设置METASO_UID和METASO_SID环境变量")

# 模型配置
MODELS = {
    "web": {
        "concise": "concise",        # 简洁模式
        "detail": "detail"           # 深入模式（默认）
    },
    "scholar": {
        "concise": "concise-scholar",  # 学术-简洁模式
        "detail": "detail-scholar"     # 学术-深入模式
    }
}

# 默认配置
DEFAULT_MODEL = "detail"  # 默认使用深入模式
DEFAULT_SCHOLAR = False   # 默认使用普通搜索

# 速率限制配置
RATE_LIMIT = {
    "per_second": 1,
    "per_minute": 60
}

request_count = {
    "second": 0,
    "minute": 0,
    "last_reset": time.time(),
    "last_minute_reset": time.time()
}

def check_rate_limit():
    """检查并更新速率限制"""
    now = time.time()
    
    # 重置秒级计数器
    if now - request_count["last_reset"] > 1:
        request_count["second"] = 0
        request_count["last_reset"] = now
        
    # 重置分钟级计数器
    if now - request_count["last_minute_reset"] > 60:
        request_count["minute"] = 0
        request_count["last_minute_reset"] = now
    
    if (request_count["second"] >= RATE_LIMIT["per_second"] or 
        request_count["minute"] >= RATE_LIMIT["per_minute"]):
        raise Exception("超出速率限制")
    
    request_count["second"] += 1
    request_count["minute"] += 1

def get_tool_descriptions() -> list[types.Tool]:
    """返回Metaso搜索工具的描述列表"""
    return [
        types.Tool(
            name="search",
            description=(
                "执行网络搜索，查找网页、新闻、文章等在线内容。"
                "支持两种模式：\n"
                "- 简洁模式：回答简短精炼\n"
                "- 深入模式：回答详细全面（默认）\n"
                "返回内容包含主要内容和参考文献。"
                "（当前使用Metaso Search API实现）"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询内容"
                    },
                    "mode": {
                        "type": "string",
                        "description": "搜索模式(concise:简洁, detail:深入)",
                        "enum": ["concise", "detail"],
                        "default": "detail"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="scholar_search",
            description=(
                "执行学术搜索，专门用于查找学术论文、研究报告等学术资源。"
                "支持两种模式：\n"
                "- 简洁模式：回答简短精炼\n"
                "- 深入模式：回答详细全面（默认）\n"
                "返回内容包含主要内容和学术参考文献。"
                "（当前使用Metaso Search API实现）"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "学术搜索查询内容"
                    },
                    "mode": {
                        "type": "string",
                        "description": "搜索模式(concise:简洁, detail:深入)",
                        "enum": ["concise", "detail"],
                        "default": "detail"
                    }
                },
                "required": ["query"]
            }
        )
    ]

# 配置 Windows asyncio 事件循环
if sys.platform == 'win32':
    # 忽略 ResourceWarning
    warnings.filterwarnings("ignore", category=ResourceWarning)

# 创建浏览器数据目录
browser_data_dir = Path(__file__).parent / "metaso/browser_data"
browser_data_dir.mkdir(parents=True, exist_ok=True)

# 创建客户端实例
client = MetasoClient(
    METASO_UID, 
    METASO_SID,
    browser_data_dir=str(browser_data_dir)
)

async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> types.TextContent:
    """统一处理工具调用"""
    if not arguments or "query" not in arguments:
        raise ValueError("缺少query参数")

    query = arguments["query"]
    mode = arguments.get("mode", DEFAULT_MODEL)
    
    if name == "search":
        results = await perform_search(query, mode, is_scholar=False)
    elif name == "scholar_search":
        results = await perform_search(query, mode, is_scholar=True)
    else:
        raise ValueError(f"Metaso搜索不支持的工具: {name}")
        
    return types.TextContent(type="text", text=results)

async def perform_search(query: str, mode: str = DEFAULT_MODEL, is_scholar: bool = DEFAULT_SCHOLAR) -> str:
    """执行搜索"""
    check_rate_limit()
    
    # 确定使用的模型
    model_type = "scholar" if is_scholar else "web"
    if mode not in MODELS[model_type]:
        raise ValueError(f"不支持的搜索模式: {mode}")
    model = MODELS[model_type][mode]
    
    try:
        # 使用MetasoClient执行搜索
        async with client as c:  # 使用上下文管理器
            result = await c.get_completion(query, model=model)
            
            # 处理返回结果
            content = result.get("content", "")
            if not content:
                raise Exception("API返回内容为空")
                
            references = result.get("references", [])
            
            # 格式化输出
            output = [content, "\n\n参考文献:"]
            
            for i, ref in enumerate(references, 1):
                output.append(
                    f"\n[{i}] {ref.get('title', '无标题')}"
                    f"\n    链接: {ref.get('link', '无链接')}"
                    f"\n    来源: {ref.get('source', '未知来源')}"
                    f"\n    日期: {ref.get('date', '未知日期')}"
                )
                
            return "\n".join(output)
            
    except Exception as e:
        raise Exception(f"搜索执行错误: {str(e)}") 