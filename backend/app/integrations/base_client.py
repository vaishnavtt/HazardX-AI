"""
HAZARDX AI — Base Resilient HTTP Client for Scientific Integrations
Provides standardized asynchronous HTTP requests, exponential backoff retries,
timeout enforcement, rate-limit awareness, and telemetry logging into SQLite api_logs.
"""

import time
import asyncio
import random
import httpx
from typing import Dict, Any, Optional, Tuple
from ..services.data_storage_service import storage_service
from ..utils.logging_config import get_logger

logger = get_logger("base_client")

class BaseResilientClient:
    def __init__(
        self,
        service_id: str,
        base_url: str,
        timeout_sec: float = 12.0,
        max_retries: int = 3,
        initial_backoff_sec: float = 0.5,
        default_headers: Optional[Dict[str, str]] = None
    ):
        self.service_id = service_id
        self.base_url = base_url
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries
        self.initial_backoff_sec = initial_backoff_sec
        self.headers = default_headers or {
            "User-Agent": f"HAZARDX-AI/1.0 (Disaster-Forecasting-Client; {service_id})"
        }

    async def get_json(
        self,
        endpoint: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True,
        cache_ttl_sec: int = 600
    ) -> Tuple[Optional[Dict[str, Any]], str, float]:
        """
        Executes a resilient GET request expecting a JSON response.
        Returns: (data_dict, provenance_status, latency_ms)
        """
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        cache_key = f"{self.service_id}_{full_url}_{str(sorted((params or {}).items()))}"

        # 1. Cache inspection
        if use_cache:
            cached = storage_service.get_cache(cache_key)
            if cached:
                logger.debug(f"[{self.service_id}] Cache hit for {full_url}")
                return cached, "CACHED_OBSERVATION", 0.5

        # 2. Resilient Execution with Backoff
        req_headers = {**self.headers, **(headers or {})}
        t0 = time.time()
        attempt = 0
        last_error = ""

        while attempt <= self.max_retries:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
                    resp = await client.get(full_url, params=params, headers=req_headers)
                    latency_ms = (time.time() - t0) * 1000

                    if resp.status_code == 200:
                        data = resp.json()
                        storage_service.log_api_call(self.service_id, 200, latency_ms, 1)
                        if use_cache:
                            storage_service.set_cache(cache_key, full_url, data, ttl_seconds=cache_ttl_sec)
                        return data, "LIVE_OBSERVATION", latency_ms
                    
                    elif resp.status_code == 429:
                        last_error = f"HTTP 429 (Rate Limited)"
                        logger.warning(f"[{self.service_id}] Rate limited on attempt {attempt}. Backing off.")
                    else:
                        last_error = f"HTTP {resp.status_code}: {resp.text[:100]}"
                        logger.warning(f"[{self.service_id}] Attempt {attempt} returned {resp.status_code}")

            except httpx.TimeoutException:
                last_error = f"Timeout ({self.timeout_sec}s exceeded)"
                logger.warning(f"[{self.service_id}] Attempt {attempt} timed out.")
            except Exception as e:
                last_error = f"Connection error: {str(e)}"
                logger.warning(f"[{self.service_id}] Attempt {attempt} failed: {e}")

            if attempt <= self.max_retries:
                # Exponential backoff with jitter
                sleep_sec = (self.initial_backoff_sec * (2 ** (attempt - 1))) + (random.random() * 0.2)
                await asyncio.sleep(sleep_sec)

        latency_ms = (time.time() - t0) * 1000
        storage_service.log_api_call(self.service_id, 500, latency_ms, 0, last_error)
        logger.error(f"[{self.service_id}] All {self.max_retries} attempts failed: {last_error}")
        return None, "UNAVAILABLE", latency_ms

    async def get_text(
        self,
        endpoint: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True,
        cache_ttl_sec: int = 900
    ) -> Tuple[Optional[str], str, float]:
        """
        Executes a resilient GET request expecting plain text/CSV.
        Returns: (text_str, provenance_status, latency_ms)
        """
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        cache_key = f"{self.service_id}_{full_url}_{str(sorted((params or {}).items()))}"

        if use_cache:
            cached = storage_service.get_cache(cache_key)
            if cached and isinstance(cached, dict) and "text" in cached:
                return cached["text"], "CACHED_OBSERVATION", 0.5

        req_headers = {**self.headers, **(headers or {})}
        t0 = time.time()
        attempt = 0
        last_error = ""

        while attempt <= self.max_retries:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
                    resp = await client.get(full_url, params=params, headers=req_headers)
                    latency_ms = (time.time() - t0) * 1000

                    if resp.status_code == 200:
                        text = resp.text
                        storage_service.log_api_call(self.service_id, 200, latency_ms, 1)
                        if use_cache:
                            storage_service.set_cache(cache_key, full_url, {"text": text}, ttl_seconds=cache_ttl_sec)
                        return text, "LIVE_OBSERVATION", latency_ms
                    else:
                        last_error = f"HTTP {resp.status_code}"
            except Exception as e:
                last_error = str(e)

            if attempt <= self.max_retries:
                sleep_sec = (self.initial_backoff_sec * (2 ** (attempt - 1))) + (random.random() * 0.2)
                await asyncio.sleep(sleep_sec)

        latency_ms = (time.time() - t0) * 1000
        storage_service.log_api_call(self.service_id, 500, latency_ms, 0, last_error)
        return None, "UNAVAILABLE", latency_ms

