"""Configuration for Brave Search API"""

import os
import time

# 检查API密钥
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    BRAVE_API_KEY = "你申请的 brave_api_key"

if not BRAVE_API_KEY:
    raise ValueError("需要设置BRAVE_API_KEY环境变量")

# 速率限制配置
RATE_LIMIT = {
    "per_second": 1,
    "per_month": 15000
}

request_count = {
    "second": 0,
    "month": 0,
    "last_reset": time.time()
}

def check_rate_limit():
    """检查并更新速率限制"""
    now = time.time()
    if now - request_count["last_reset"] > 1:
        request_count["second"] = 0
        request_count["last_reset"] = now
    
    if (request_count["second"] >= RATE_LIMIT["per_second"] or 
        request_count["month"] >= RATE_LIMIT["per_month"]):
        raise Exception("超出速率限制")
    
    request_count["second"] += 1
    request_count["month"] += 1 