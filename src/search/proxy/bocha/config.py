"""Configuration for Bocha Search API

This module contains configuration settings and constants for the Bocha Search API.

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

import os
import time
from typing import Dict

# API配置
BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "")
if not BOCHA_API_KEY:
    BOCHA_API_KEY="你申请的 bocha_api_key"

API_ENDPOINT = "https://api.bochaai.com/v1/web-search?utm_source=search-mcp-server"

# 搜索时间范围配置
FRESHNESS_RANGES: Dict[str, str] = {
    "noLimit": "noLimit",     # 不限
    "oneDay": "oneDay",       # 一天内
    "oneWeek": "oneWeek",     # 一周内
    "oneMonth": "oneMonth",   # 一个月内
    "oneYear": "oneYear"      # 一年内
}

# 默认配置
DEFAULT_COUNT = 10            # 默认返回结果数
DEFAULT_FRESHNESS = "noLimit" # 默认时间范围
DEFAULT_SUMMARY = False       # 默认不显示摘要
DEFAULT_PAGE = 1             # 默认页码

# 速率限制配置
RATE_LIMIT = {
    "per_second": 2,
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

def validate_api_key() -> None:
    """验证API密钥是否有效
    
    Raises:
        ValueError: 当API密钥无效或未设置时
    """
    if not BOCHA_API_KEY:
        raise ValueError(
            "未设置BOCHA_API_KEY环境变量。"
            "请在.env文件中设置BOCHA_API_KEY=your_api_key"
        ) 