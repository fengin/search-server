"""Brave Search API client implementation

This module provides the core client functionality for interacting with Brave Search API.
"""

import httpx
from typing import Dict, Any, List, Optional
import os
from .exceptions import BraveException
from .config import BRAVE_API_KEY, check_rate_limit

class BraveClient:
    """Brave Search API客户端
    
    提供网络搜索和位置搜索功能的客户端实现。
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化客户端
        
        Args:
            api_key: Brave Search API密钥，如果不提供则使用环境变量
        """
        self.api_key = api_key or BRAVE_API_KEY
        if not self.api_key:
            raise BraveException("需要提供API密钥")
            
    async def web_search(self, query: str, count: int = 10, offset: int = 0) -> List[Dict[str, str]]:
        """执行网络搜索
        
        Args:
            query: 搜索查询
            count: 结果数量(1-20)
            offset: 分页偏移量(最大9)
            
        Returns:
            List[Dict]: 搜索结果列表，每个结果包含title、description和url
        """
        check_rate_limit()
        
        url = "https://api.search.brave.com/res/v1/web/search"
        params = {
            "q": query,
            "count": min(count, 20),
            "offset": offset
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers=self._get_headers()
            )
            
            if response.status_code != 200:
                raise BraveException(f"API错误: {response.status_code} {response.text}")
                
            data = response.json()
            results = []
            for result in data.get("web", {}).get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "description": result.get("description", ""),
                    "url": result.get("url", "")
                })
                
            return results
            
    async def location_search(self, query: str, count: int = 5) -> List[Dict[str, Any]]:
        """执行地理位置搜索
        
        Args:
            query: 位置搜索查询
            count: 结果数量(1-20)
            
        Returns:
            List[Dict]: 位置搜索结果列表
        """
        check_rate_limit()
        
        # 初始搜索获取位置ID
        web_url = "https://api.search.brave.com/res/v1/web/search"
        params = {
            "q": query,
            "search_lang": "en",
            "result_filter": "locations",
            "count": min(count, 20)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                web_url,
                params=params,
                headers=self._get_headers()
            )
            
            if response.status_code != 200:
                raise BraveException(f"API错误: {response.status_code} {response.text}")
                
            data = response.json()
            location_ids = [
                r["id"] for r in data.get("locations", {}).get("results", [])
                if "id" in r
            ]
            
            if not location_ids:
                # 如果没有位置结果，返回网络搜索结果
                return await self.web_search(query, count)
                
            # 并行获取POI详情和描述
            pois_url = "https://api.search.brave.com/res/v1/local/pois"
            desc_url = "https://api.search.brave.com/res/v1/local/descriptions"
            
            pois_response = await client.get(
                pois_url,
                params={"ids": location_ids},
                headers=self._get_headers()
            )
            
            desc_response = await client.get(
                desc_url,
                params={"ids": location_ids},
                headers=self._get_headers()
            )
            
            if pois_response.status_code != 200 or desc_response.status_code != 200:
                raise BraveException("获取POI详情或描述失败")
                
            pois_data = pois_response.json()
            desc_data = desc_response.json()
            
            results = []
            for poi in pois_data.get("results", []):
                address_parts = [
                    poi.get("address", {}).get("streetAddress", ""),
                    poi.get("address", {}).get("addressLocality", ""),
                    poi.get("address", {}).get("addressRegion", ""),
                    poi.get("address", {}).get("postalCode", "")
                ]
                address = ", ".join(filter(None, address_parts))
                
                rating = poi.get("rating", {})
                description = desc_data.get("descriptions", {}).get(poi["id"], "暂无描述")
                
                results.append({
                    "name": poi.get("name", "暂无"),
                    "address": address or "暂无",
                    "phone": poi.get("phone", "暂无"),
                    "rating": {
                        "value": rating.get("ratingValue", "暂无"),
                        "count": rating.get("ratingCount", 0)
                    },
                    "price_range": poi.get("priceRange", "暂无"),
                    "opening_hours": poi.get("openingHours", []),
                    "description": description
                })
                
            return results
            
    def _get_headers(self) -> Dict[str, str]:
        """获取API请求头
        
        Returns:
            Dict[str, str]: 请求头字典
        """
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        } 