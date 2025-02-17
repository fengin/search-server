#描述：基于即梦AI的图像生成服务，专门设计用于与Cursor IDE集成。它接收来自Cursor的文本描述，生成相应的图像，并提供图片下载和保存功能。
#作者：凌封 (微信fengin)
#GITHUB: https://github.com/fengin/search-server.git
#相关知识可以看AI全书：https://aibook.ren 

from typing import Any, Dict, List, Optional
import asyncio
import os
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from sys import stdin, stdout

# mcp核心协议源码对unicode编码处理还有bug，需手动指定为utf-8
stdin.reconfigure(encoding='utf-8')
stdout.reconfigure(encoding='utf-8')

# 导入搜索引擎模块
from .proxy.brave_search import (
    handle_tool_call as brave_handle_tool,
    get_tool_descriptions as brave_tools
)
from .proxy.metaso_search import (
    handle_tool_call as metaso_handle_tool,
    get_tool_descriptions as metaso_tools
)
from .proxy.bocha_search import (
    handle_tool_call as bocha_handle_tool,
    get_tool_descriptions as bocha_tools
)

# 搜索引擎配置
SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "bocha")
AVAILABLE_ENGINES = {
    "brave": {
        "handle_tool": brave_handle_tool,
        "tools": brave_tools,
        "description": "Brave Search API，支持网络搜索和位置搜索"
    },
    "metaso": {
        "handle_tool": metaso_handle_tool,
        "tools": metaso_tools,
        "description": "Metaso Search API，支持网络搜索和学术搜索，提供简洁、深入、研究三种模式"
    },
    "bocha": {
        "handle_tool": bocha_handle_tool,
        "tools": bocha_tools,
        "description": "博查搜索API，支持网络搜索，提供时间范围过滤、详细摘要等功能"
    }
}

if SEARCH_ENGINE not in AVAILABLE_ENGINES:
    raise ValueError(
        f"不支持的搜索引擎: {SEARCH_ENGINE}\n"
        f"可用的搜索引擎:\n" + 
        "\n".join(f"- {name}: {engine['description']}" 
                 for name, engine in AVAILABLE_ENGINES.items())
    )

server = Server("search")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用的搜索工具"""
    return AVAILABLE_ENGINES[SEARCH_ENGINE]["tools"]()

@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: Optional[Dict[str, Any]]
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用请求"""
    try:
        if not arguments:
            raise ValueError("缺少参数")
            
        result = await AVAILABLE_ENGINES[SEARCH_ENGINE]["handle_tool"](name, arguments)
        return [result]
            
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