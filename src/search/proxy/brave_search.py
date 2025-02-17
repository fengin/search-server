"""Brave Search API implementation for MCP server

This module provides web search and location-based search functionality using Brave Search API.
It includes the MCP tool descriptions and handlers.
"""

from typing import Dict, Any
import mcp.types as types
from .brave import BraveClient, BraveException

def get_tool_descriptions() -> list[types.Tool]:
    """返回Brave搜索工具的描述列表"""
    return [
        types.Tool(
            name="search",
            description=(
                "执行网络搜索，查找网页、新闻、文章等在线内容。"
                "适合广泛的信息收集、近期事件，或需要多样化网络来源时使用。"
                "支持分页、内容过滤和时效性控制。"
                "每次请求最多返回20个结果，支持分页偏移。"
                "（当前使用Brave Search API实现）"
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
            name="location_search",
            description=(
                "搜索地理位置相关的信息，如商家、餐厅、服务等。"
                "返回详细信息包括:\n"
                "- 商家名称和地址\n"
                "- 评分和评论数\n"
                "- 电话号码和营业时间\n"
                "适用于查询特定地点或位置相关的信息，"
                "如果没有找到相关结果会自动切换到普通网络搜索。"
                "（当前使用Brave Search API实现）"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "位置搜索查询(例如:'上海东方明珠附近的餐厅')"
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

async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> types.TextContent:
    """统一处理工具调用"""
    if not arguments or "query" not in arguments:
        raise ValueError("缺少query参数")

    query = arguments["query"]
    client = BraveClient()
    
    try:
        if name == "search":
            count = arguments.get("count", 10)
            offset = arguments.get("offset", 0)
            results = await client.web_search(query, count, offset)
            
            # 格式化输出
            formatted_results = []
            for result in results:
                formatted_results.append(
                    f"标题: {result['title']}\n"
                    f"描述: {result['description']}\n"
                    f"网址: {result['url']}"
                )
                
            return types.TextContent(
                type="text",
                text="\n\n".join(formatted_results)
            )
            
        elif name == "location_search":
            count = arguments.get("count", 5)
            results = await client.location_search(query, count)
            
            # 检查是否为网络搜索结果
            if results and "url" in results[0]:
                # 如果是网络搜索结果，使用网络搜索格式
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        f"标题: {result['title']}\n"
                        f"描述: {result['description']}\n"
                        f"网址: {result['url']}"
                    )
            else:
                # 如果是位置搜索结果，使用位置信息格式
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        f"名称: {result['name']}\n"
                        f"地址: {result['address']}\n"
                        f"电话: {result['phone']}\n"
                        f"评分: {result['rating']['value']} ({result['rating']['count']}条评论)\n"
                        f"价格范围: {result['price_range']}\n"
                        f"营业时间: {', '.join(result['opening_hours']) or '暂无'}\n"
                        f"描述: {result['description']}"
                    )
                    
            return types.TextContent(
                type="text",
                text="\n---\n".join(formatted_results) if formatted_results else "未找到相关结果"
            )
            
        else:
            raise ValueError(f"Brave搜索不支持的工具: {name}")
            
    except BraveException as e:
        return types.TextContent(
            type="text",
            text=f"搜索执行错误: {str(e)}"
        ) 