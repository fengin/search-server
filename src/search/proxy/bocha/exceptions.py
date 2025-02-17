"""Bocha Search API exceptions

This module defines exceptions for the Bocha Search API client.

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

from typing import Dict, Type

class BochaException(Exception):
    """博查搜索API异常基类"""
    pass

class BochaAPIError(BochaException):
    """API调用错误"""
    pass

class BochaRateLimitError(BochaException):
    """速率限制错误"""
    pass

class BochaAuthError(BochaException):
    """认证错误"""
    pass

class BochaBalanceError(BochaException):
    """余额不足错误"""
    pass

class BochaRequestError(BochaException):
    """请求错误"""
    pass

class BochaResponseError(BochaException):
    """响应解析错误"""
    pass

# 错误码映射
ERROR_CODE_MAP: Dict[str, Type[BochaException]] = {
    "400": BochaAPIError,        # 请求参数错误
    "401": BochaAuthError,       # 认证错误
    "403": BochaBalanceError,    # 余额不足
    "429": BochaRateLimitError,  # 速率限制
    "500": BochaAPIError         # 服务器错误
}

def raise_for_error_code(code: str, message: str) -> None:
    """根据错误码抛出对应的异常
    
    Args:
        code: API返回的错误码
        message: 错误消息
        
    Raises:
        BochaException: 对应的异常类型
    """
    exception_class = ERROR_CODE_MAP.get(code, BochaAPIError)
    raise exception_class(f"API错误 {code}: {message}") 