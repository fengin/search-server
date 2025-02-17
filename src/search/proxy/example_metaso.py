#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MetaSo API 使用示例

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）

这个示例展示了如何使用 MetaSo API 进行对话。包括:
1. 基本的客户端初始化
2. 非流式对话
3. 流式对话
4. 错误处理

使用前请先安装依赖:
pip install -r requirements.txt

可以通过以下方式运行示例：
切换到 src/search/proxy/metaso 目录
执行 python -m example_metaso

"""

import asyncio
import logging
import warnings
import sys
from contextlib import suppress
from typing import List

# 配置 Windows asyncio 事件循环
if sys.platform == 'win32':
    # 忽略 ResourceWarning
    warnings.filterwarnings("ignore", category=ResourceWarning)

from . import MetasoClient
from .client import SUPPORTED_MODELS
from .exceptions import MetasoException

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 测试用的凭证
# 注意: 这里的值仅用于演示，实际使用时请替换为你自己的凭证
UID = "67b0341c6ea***9a9be263f"
SID = "b8fb1b5a22a*******06aae5a44d"
# 自定义浏览器数据目录
BROWSER_DATA_DIR = "custom_browser_data"

async def verify_credentials(uid: str, sid: str) -> bool:
    """验证凭证是否有效
    
    Args:
        uid: 用户ID
        sid: 会话ID
        
    Returns:
        bool: 凭证是否有效
    """
    try:
        async with MetasoClient(uid, sid) as client:
            # 尝试获取 meta token
            await client._get_meta_token()
            return True
    except MetasoException as e:
        logger.error(f"凭证验证失败: {e}")
        return False
    except Exception as e:
        logger.error(f"验证过程出错: {e}")
        return False

async def demo_normal_chat():
    """演示普通对话(非流式)
    
    这个函数展示了如何使用非流式方式进行对话。
    非流式方式会等待完整的回复后一次性返回。
    """
    try:
        # 使用自定义浏览器数据目录
        async with MetasoClient(UID, SID, browser_data_dir=BROWSER_DATA_DIR) as client:
            # 准备对话内容
            messages = [
                "介绍一下杭州西湖的主要景点"
            ]
            
            # 对每个消息进行对话
            for message in messages:
                logger.info(f"发送消息: {message}")
                try:
                    # 使用默认模型(detail)进行对话
                    response = await client.get_completion(message)
                    logger.info(f"收到回复: {response}")
                except MetasoException as e:
                    logger.error(f"对话失败: {e}")
                    
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def demo_stream_chat():
    """演示流式对话
    
    这个函数展示了如何使用流式方式进行对话。
    流式方式会实时返回生成的内容，适合需要实时展示的场景。
    """
    try:
        async with MetasoClient(UID, SID) as client:
            message = "详细介绍杭州西湖十景"
            logger.info(f"发送消息: {message}")
            
            try:
                # 使用 research 模型进行流式对话
                print("接收回复: ", end="", flush=True)
                async for chunk in client.get_completion_stream(message, model="research"):
                    print(chunk, end="", flush=True)
                print()  # 换行
            except MetasoException as e:
                logger.error(f"流式对话失败: {e}")
                
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def demo_different_models():
    """演示使用不同的模型
    
    这个函数展示了如何使用不同的模型进行对话。
    MetaSo 提供了多种模型，每种模型有其特点：
    - concise: 简洁模式，回答简短精炼
    - detail: 深入模式，回答详细全面
    - research: 研究模式，回答深度分析
    """
    try:
        # 使用单个客户端实例处理所有请求
        async with MetasoClient(UID, SID) as client:
            message = "介绍一下西湖断桥残雪的景色"
            
            # 使用不同模型
            for model in ["concise", "detail", "research"]:
                logger.info(f"\n使用 {model} 模型:")
                # 添加重试逻辑
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = await client.get_completion(message, model=model)
                        logger.info(f"回复: {response}")
                        break  # 成功后跳出重试循环
                    except MetasoException as e:
                        if attempt == max_retries - 1:  # 最后一次尝试
                            logger.error(f"使用 {model} 模型失败: {e}")
                        else:
                            logger.warning(f"第 {attempt + 1} 次尝试失败，正在重试...")
                            await asyncio.sleep(1)  # 重试前等待
                    except Exception as e:
                        logger.error(f"使用 {model} 模型时发生未知错误: {e}")
                        break  # 遇到未知错误直接跳出
                    
    except Exception as e:
        logger.error(f"执行过程出错: {e}")

async def main():
    """主函数，按顺序运行所有演示"""
    try:
        # 验证凭证
        if not await verify_credentials(UID, SID):
            logger.error("请确保 UID 和 SID 有效")
            return
            
        # 运行非流式对话演示
        logger.info("\n=== 演示普通对话 ===")
        await demo_normal_chat()
        
        # 等待一下，避免请求太频繁
        await asyncio.sleep(1)
        
        # 运行流式对话演示
        logger.info("\n=== 演示流式对话 ===")
        await demo_stream_chat()
        
        # 等待一下，避免请求太频繁
        await asyncio.sleep(1)
        
        # 运行不同模型演示
        logger.info("\n=== 演示不同模型 ===")
        await demo_different_models()
        
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