#描述：基于即梦AI的图像生成服务，专门设计用于与Cursor IDE集成。它接收来自Cursor的文本描述，生成相应的图像，并提供图片下载和保存功能。
#作者：凌封 (微信fengin)
#GITHUB: https://github.com/fengin/search-server.git
#相关知识可以看AI全书：https://aibook.ren 


from . import server
import asyncio

def main():
    """包的主入口点。"""
    asyncio.run(server.main())

# 可选：在包级别暴露其他重要项
__all__ = ['main', 'server']
