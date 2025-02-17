"""
异常定义

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

class MetasoException(Exception):
    """Base exception for Metaso client."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

# 定义错误码常量
API_TEST = (-9999, 'API异常错误')
API_REQUEST_PARAMS_INVALID = (-2000, '请求参数非法')
API_REQUEST_FAILED = (-2001, '请求失败')
API_TOKEN_EXPIRES = (-2002, 'Token已失效')
API_FILE_URL_INVALID = (-2003, '远程文件URL非法')
API_FILE_EXECEEDS_SIZE = (-2004, '远程文件超出大小')
API_CHAT_STREAM_PUSHING = (-2005, '已有对话流正在输出')
API_CONTENT_FILTERED = (-2006, '内容由于合规问题已被阻止生成')
API_IMAGE_GENERATION_FAILED = (-2007, '图像生成失败')
API_CONTENT_EMPTY = (-2008, '消息不能为空') 