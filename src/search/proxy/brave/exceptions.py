"""Brave Search API exceptions"""

class BraveException(Exception):
    """Brave Search API异常基类"""
    pass

class BraveAPIError(BraveException):
    """API调用错误"""
    pass

class BraveRateLimitError(BraveException):
    """速率限制错误"""
    pass 