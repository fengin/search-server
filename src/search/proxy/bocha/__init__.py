"""Bocha Search API Client Package

This package provides a Python interface for the Bocha Search API.
It includes a client for making API requests and handling responses.

作者: 凌封（微信：fengin）
网站: AI全书（https://aibook.ren）
"""

from .client import BochaClient
from .exceptions import (
    BochaException,
    BochaAPIError,
    BochaRateLimitError,
    BochaAuthError,
    BochaBalanceError
)
from .config import (
    BOCHA_API_KEY,
    FRESHNESS_RANGES,
    check_rate_limit,
    validate_api_key
)

__all__ = [
    'BochaClient',
    'BochaException',
    'BochaAPIError', 
    'BochaRateLimitError',
    'BochaAuthError',
    'BochaBalanceError',
    'BOCHA_API_KEY',
    'FRESHNESS_RANGES',
    'check_rate_limit',
    'validate_api_key'
]

__version__ = '0.1.0' 