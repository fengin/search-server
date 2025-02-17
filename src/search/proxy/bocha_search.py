"""Bocha Search API implementation for MCP server

This module provides web search functionality using Bocha Search API.
It includes the MCP tool descriptions and handlers.

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

from typing import Dict, Any
import mcp.types as types
from .bocha import BochaClient, BochaException, FRESHNESS_RANGES

def get_tool_descriptions() -> list[types.Tool]:
    """返回博查搜索工具的描述列表"""
    return [
        types.Tool(
            name="search",
            description=(
                "执行网页搜索，从全网搜索任何网页信息和网页链接。"
                "结果准确、摘要完整，更适合AI使用。"
                "支持以下特性：\n"
                "- 时间范围过滤\n"
                "- 显示详细摘要\n"
                "- 分页获取\n"
                "每次请求最多返回10个结果。"
                "（当前使用博查搜索API实现）"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询内容"
                    },
                    "count": {
                        "type": "number",
                        "description": "结果数量(1-10，默认10)",
                        "default": 10
                    },
                    "page": {
                        "type": "number",
                        "description": "页码，从1开始",
                        "default": 1
                    },
                    "freshness": {
                        "type": "string",
                        "description": "时间范围(noLimit:不限, oneDay:一天内, oneWeek:一周内, oneMonth:一月内, oneYear:一年内)",
                        "enum": list(FRESHNESS_RANGES.values()),
                        "default": "noLimit"
                    },
                    "summary": {
                        "type": "boolean",
                        "description": "是否显示详细摘要",
                        "default": False
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
    client = BochaClient()
    
    try:
        if name == "search":
            count = arguments.get("count", 10)
            page = arguments.get("page", 1)
            freshness = arguments.get("freshness", "noLimit")
            summary = arguments.get("summary", False)
            
            response = await client.web_search(
                query=query,
                count=count,
                page=page,
                freshness=freshness,
                summary=summary
            )
            
            # 检查响应状态
            if response.get("code") != 200:
                return types.TextContent(
                    type="text",
                    text=f"搜索失败: {response.get('msg', '未知错误')}"
                )
                
            # 获取搜索结果数据
            data = response.get("data", {})
            if not data:
                return types.TextContent(
                    type="text",
                    text="未找到相关结果"
                )
                
            # 格式化输出
            formatted_results = []
            
            # 首先添加统计信息
            web_pages = data.get("webPages", {})
            total_results = web_pages.get("totalEstimatedMatches", 0)
            current_results = len(web_pages.get("value", []))
            total_pages = (total_results + count - 1) // count if total_results > 0 else 0
            
            formatted_results.extend([
                "搜索统计信息:",
                f"- 总结果数: {total_results:,} 条",
                f"- 当前页/总页数: {page}/{total_pages}",
                f"- 本页结果数: {current_results} 条",
                ""  # 添加空行分隔
            ])
            
            # 处理网页结果
            web_pages = data.get("webPages", {}).get("value", [])
            for result in web_pages:
                content = [
                    f"标题: {result.get('name', '')}",
                    f"网址: {result.get('url', '')}",
                    f"来源: {result.get('siteName', '未知来源')}"
                ]
                
                # 如果有摘要，添加摘要信息
                if summary and "summary" in result:
                    content.append(f"摘要: {result['summary']}")
                else:
                    content.append(f"描述: {result.get('snippet', '')}")
                    
                # 如果有发布时间，添加时间信息
                if "dateLastCrawled" in result:
                    content.append(f"发布时间: {result['dateLastCrawled']}")
                    
                formatted_results.append("\n".join(content))
                
            # 如果有图片结果，添加图片信息
            images = data.get("images", {}).get("value", [])
            if images:
                formatted_results.append("\n相关图片:")
                for image in images:
                    image_info = [
                        f"- 名称: {image.get('name', '未命名')}",
                        f"  尺寸: {image.get('width', '未知')}x{image.get('height', '未知')}",
                        f"  来源页面: {image.get('hostPageDisplayUrl', image.get('hostPageUrl', '未知'))}",
                        f"  原图URL: {image.get('contentUrl', '')}",
                        f"  缩略图URL: {image.get('thumbnailUrl', '')}"
                    ]
                    formatted_results.append("\n".join(image_info))
                    
            return types.TextContent(
                type="text",
                text="\n\n".join(formatted_results) if formatted_results else "未找到相关结果"
            )
            
        else:
            raise ValueError(f"博查搜索不支持的工具: {name}")
            
    except BochaException as e:
        return types.TextContent(
            type="text",
            text=f"搜索执行错误: {str(e)}"
        ) 