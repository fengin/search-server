"""
Brave Search API client implementation.
This module provides the core client functionality for interacting with Brave Search API.
"""

from .client import BraveClient
from .exceptions import BraveException, BraveAPIError, BraveRateLimitError
from .config import BRAVE_API_KEY, check_rate_limit

__all__ = [
    'BraveClient',
    'BraveException',
    'BraveAPIError',
    'BraveRateLimitError',
    'BRAVE_API_KEY',
    'check_rate_limit'
] 