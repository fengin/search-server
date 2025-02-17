#描述：基于即梦AI的图像生成服务，专门设计用于与Cursor IDE集成。它接收来自Cursor的文本描述，生成相应的图像，并提供图片下载和保存功能。
#作者：凌封 (微信fengin)
#GITHUB: https://github.com/fengin/search-server.git
#相关知识可以看AI全书：https://aibook.ren 

'''
如果配置运行不起来，可以尝试配置这个MCP Server
这仅是一个类似Hello World的示例，实现了最基本MCP Server框架
'''

from typing import Any
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from sys import stdin, stdout

# mcp核心协议源码对unicode编码处理还有bug，需手动指定为utf-8
stdin.reconfigure(encoding='utf-8')
stdout.reconfigure(encoding='utf-8')

server = Server("search")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用的工具。
    每个工具使用 JSON Schema 验证来指定其参数。
    """
    return [
        types.Tool(
            name="search-by-key",
            description="通地关键词搜索网络资料",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "关键词",
                    },
                },
                "required": ["key"],
            },
        )
    ]
    
@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理工具执行请求。
    工具可以获取天气数据并通知客户端变化。
    """
    if not arguments:
        raise ValueError("缺少参数")
        
    if name == "search-by-key":
        key = arguments.get("key")
        alerts_text = f"搜索的内容是{key} "
        return [
                types.TextContent(
                    type="text",
                    text=alerts_text
                )
            ]
    else:
        raise ValueError(f"未知工具: {name}")


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