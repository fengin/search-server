"""Configuration for Metaso Search API"""

import os
import time

# 认证信息
METASO_UID = os.getenv("METASO_UID")
METASO_SID = os.getenv("METASO_SID")
if not METASO_UID or not METASO_SID:
    METASO_UID = "你获取的 metaso uid"
    METASO_SID = "你获取的 metaso sid"

if not METASO_UID or not METASO_SID:
    raise ValueError("需要设置METASO UID和METASO SID环境变量")

# 模型配置
MODELS = {
    "web": {
        "concise": "concise",        # 简洁模式
        "detail": "detail"           # 深入模式（默认）
    },
    "scholar": {
        "concise": "concise-scholar",  # 学术-简洁模式
        "detail": "detail-scholar"     # 学术-深入模式
    }
}

# 默认配置
DEFAULT_MODEL = "detail"  # 默认使用深入模式
DEFAULT_SCHOLAR = False   # 默认使用普通搜索

# 速率限制配置
RATE_LIMIT = {
    "per_second": 1,
    "per_minute": 60
}

request_count = {
    "second": 0,
    "minute": 0,
    "last_reset": time.time(),
    "last_minute_reset": time.time()
}

def check_rate_limit():
    """检查并更新速率限制"""
    now = time.time()
    
    # 重置秒级计数器
    if now - request_count["last_reset"] > 1:
        request_count["second"] = 0
        request_count["last_reset"] = now
        
    # 重置分钟级计数器
    if now - request_count["last_minute_reset"] > 60:
        request_count["minute"] = 0
        request_count["last_minute_reset"] = now
    
    if (request_count["second"] >= RATE_LIMIT["per_second"] or 
        request_count["minute"] >= RATE_LIMIT["per_minute"]):
        raise Exception("超出速率限制")
    
    request_count["second"] += 1
    request_count["minute"] += 1 