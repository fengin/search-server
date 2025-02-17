"""Bocha Search API client implementation

This module provides the core client functionality for interacting with Bocha Search API.

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

import httpx
from typing import Dict, Any, List, Optional
import json
from .exceptions import (
    BochaException, BochaRequestError, 
    BochaResponseError, raise_for_error_code
)
from .config import (
    BOCHA_API_KEY, API_ENDPOINT, FRESHNESS_RANGES,
    DEFAULT_COUNT, DEFAULT_FRESHNESS, DEFAULT_SUMMARY,
    DEFAULT_PAGE, check_rate_limit
)

class BochaClient:
    """博查搜索API客户端
    
    提供网页搜索功能，支持时间范围过滤和摘要显示。
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化客户端
        
        Args:
            api_key: 博查搜索API密钥，如果不提供则使用环境变量
        """
        self.api_key = api_key or BOCHA_API_KEY
        if not self.api_key:
            raise BochaException("需要提供API密钥")
            
    async def web_search(
        self, 
        query: str, 
        count: int = DEFAULT_COUNT,
        page: int = DEFAULT_PAGE,
        freshness: str = DEFAULT_FRESHNESS,
        summary: bool = DEFAULT_SUMMARY
    ) -> Dict[str, Any]:
        """执行网页搜索
        
        Args:
            query: 搜索查询
            count: 结果数量(1-10)
            page: 页码，从1开始
            freshness: 时间范围，可选值见FRESHNESS_RANGES
            summary: 是否显示摘要
            
        Returns:
            Dict: 完整的API响应
            
        Raises:
            BochaException: API调用出错
            BochaRequestError: 请求发送失败
            BochaResponseError: 响应解析失败
        """
        check_rate_limit()
        
        # 验证参数
        if not query:
            raise ValueError("搜索查询不能为空")
        if not 1 <= count <= 10:
            raise ValueError("count必须在1-10之间")
        if page < 1:
            raise ValueError("page必须大于0")
        if freshness not in FRESHNESS_RANGES.values():
            raise ValueError(f"freshness必须是以下值之一: {list(FRESHNESS_RANGES.values())}")
            
        # 准备请求数据
        data = {
            "query": query,
            "count": count,
            "page": page,
            "freshness": freshness,
            "summary": summary
        }
        
        # 发送请求
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    API_ENDPOINT,
                    json=data,
                    headers=self._get_headers()
                )
                
                # 解析响应数据
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    raise BochaResponseError("API返回数据解析失败")
                
                # 检查响应状态
                if response.status_code != 200:
                    raise_for_error_code(
                        str(response_data.get("code", "unknown")),
                        response_data.get("msg", "未知错误")
                    )
                
                # 验证响应格式
                if not isinstance(response_data, dict):
                    raise BochaResponseError("API返回数据格式错误")
                    
                # 返回完整响应
                return response_data
                
            except httpx.RequestError as e:
                raise BochaRequestError(f"请求失败: {str(e)}")
            
    def _get_headers(self) -> Dict[str, str]:
        """获取API请求头
        
        Returns:
            Dict[str, str]: 请求头字典
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 