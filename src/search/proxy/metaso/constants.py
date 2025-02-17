"""
常量定义

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

# 默认模型名称
DEFAULT_MODEL = "detail"

# 最大重试次数
MAX_RETRY_COUNT = 3

# 重试延迟(秒)
RETRY_DELAY = 5

# 伪装headers
FAKE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://metaso.cn",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# API URLs
BASE_URL = "https://metaso.cn"
API_SEARCH_URL = f"{BASE_URL}/api/searchV2"
API_SESSION_URL = f"{BASE_URL}/api/session"
API_MY_INFO_URL = f"{BASE_URL}/api/my-info"

# 支持的模型列表
SUPPORTED_MODELS = [
    "concise",         # 简洁模式
    "detail",          # 深入模式
    "research",        # 研究模式
    "concise-scholar", # 学术-简洁模式
    "detail-scholar",  # 学术-深入模式
    "research-scholar" # 学术-研究模式
] 