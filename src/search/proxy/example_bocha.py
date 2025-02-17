#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
博查搜索 API 使用示例

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）

这个示例展示了如何使用博查搜索 API 进行搜索。包括:
1. 基本的客户端初始化
2. 基础搜索功能
3. 高级搜索选项
4. 错误处理

使用方法:
1. 安装依赖:
   pip install -r requirements.txt

2. 运行示例:
   python example_bocha.py
"""

import os
import sys
import asyncio
import logging
import warnings
from typing import Dict, Any

# 配置 Windows asyncio 事件循环
if sys.platform == 'win32':
    # 忽略 ResourceWarning
    warnings.filterwarnings("ignore", category=ResourceWarning)

# 导入博查搜索模块
from bocha import client, exceptions, config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 测试用的API密钥
API_KEY = "sk-0f07fa*****aaa2bea384b"  # 替换为你的API密钥

async def verify_api_key(api_key: str) -> bool:
    """验证API密钥是否有效
    
    Args:
        api_key: API密钥
        
    Returns:
        bool: API密钥是否有效
    """
    try:
        client_obj = client.BochaClient(api_key)
        # 尝试执行一个简单的搜索
        await client_obj.web_search("test", count=1)
        return True
    except exceptions.BochaException as e:
        logger.error(f"API密钥验证失败: {e}")
        return False
    except Exception as e:
        logger.error(f"验证过程出错: {e}")
        return False

async def demo_basic_search():
    """演示基本搜索功能
    
    这个函数展示了如何使用基本的搜索功能。
    包括设置结果数量和页码。
    """
    try:
        client_obj = client.BochaClient(API_KEY)
        
        # 准备搜索内容
        queries = [
            "杭州西湖十景",
            "人工智能发展历史",
            "中国传统节日"
        ]
        
        # 对每个查询进行搜索
        for query in queries:
            logger.info(f"\n执行搜索: {query}")
            try:
                # 使用基本搜索
                response = await client_obj.web_search(
                    query=query,
                    count=5  # 获取5条结果
                )
                
                # 处理搜索结果
                results = response.get("data", {}).get("webPages", {}).get("value", [])
                for result in results:
                    logger.info(
                        f"\n标题: {result.get('name')}\n"
                        f"网址: {result.get('url')}\n"
                        f"描述: {result.get('snippet')}\n"
                    )
                    
            except exceptions.BochaException as e:
                logger.error(f"搜索失败: {e}")
                
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def demo_advanced_search():
    """演示高级搜索功能
    
    这个函数展示了如何使用高级搜索选项。
    包括时间范围过滤和详细摘要。
    """
    try:
        client_obj = client.BochaClient(API_KEY)
        query = "2024年春节"
        
        # 使用不同的时间范围
        for freshness in config.FRESHNESS_RANGES:
            logger.info(f"\n使用时间范围 {freshness}:")
            try:
                response = await client_obj.web_search(
                    query=query,
                    count=3,
                    freshness=freshness,
                    summary=True  # 显示详细摘要
                )
                
                # 处理搜索结果
                results = response.get("data", {}).get("webPages", {}).get("value", [])
                for result in results:
                    logger.info(
                        f"\n标题: {result.get('name')}\n"
                        f"时间: {result.get('dateLastCrawled')}\n"
                        f"摘要: {result.get('summary', result.get('snippet'))}\n"
                    )
                    
            except exceptions.BochaException as e:
                logger.error(f"使用 {freshness} 搜索失败: {e}")
                
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def demo_error_handling():
    """演示错误处理
    
    这个函数展示了如何处理各种可能的错误情况。
    """
    try:
        # 使用无效的API密钥
        logger.info("\n测试无效的API密钥:")
        client_obj = client.BochaClient("invalid_key")
        try:
            await client_obj.web_search("test")
        except exceptions.BochaException as e:
            logger.info(f"预期的认证错误: {e}")
            
        # 使用有效的API密钥
        client_obj = client.BochaClient(API_KEY)
        
        # 测试无效的参数
        logger.info("\n测试无效的参数:")
        try:
            await client_obj.web_search("", count=0)
        except ValueError as e:
            logger.info(f"预期的参数错误: {e}")
            
        # 测试无效的时间范围
        logger.info("\n测试无效的时间范围:")
        try:
            await client_obj.web_search("test", freshness="invalid")
        except ValueError as e:
            logger.info(f"预期的参数错误: {e}")
            
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def main():
    """主函数，按顺序运行所有演示"""
    try:
        # 验证API密钥
        if not await verify_api_key(API_KEY):
            logger.error("请确保API密钥有效")
            return
            
        # 运行基本搜索演示
        logger.info("\n=== 演示基本搜索 ===")
        await demo_basic_search()
        
        # 等待一下，避免请求太频繁
        await asyncio.sleep(1)
        
        # 运行高级搜索演示
        logger.info("\n=== 演示高级搜索 ===")
        await demo_advanced_search()
        
        # 等待一下，避免请求太频繁
        await asyncio.sleep(1)
        
        # 运行错误处理演示
        logger.info("\n=== 演示错误处理 ===")
        await demo_error_handling()
        
    except Exception as e:
        logger.error(f"主函数执行出错: {e}")
        raise  # 重新抛出异常，确保程序正确退出

if __name__ == "__main__":
    try:
        # 运行异步主函数
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
    finally:
        # 不再需要手动清理资源，asyncio.run() 会处理清理工作
        pass 