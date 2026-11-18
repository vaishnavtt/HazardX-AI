"""
HAZARDX AI — Ingestion & Forecasting Background Scheduler
Executes periodic data retrieval, freshness checks, and alert evaluations with
asyncio lock protection to prevent concurrent duplicate execution.
"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from .ingestion_manager import ingestion_manager
from ..utils.logging_config import get_logger

logger = get_logger("scheduler")

class IngestionScheduler:
    def __init__(self, interval_sec: int = 300):
        self.interval_sec = interval_sec
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self.last_run_time: Optional[str] = None
        self.last_run_summary: Optional[Dict[str, Any]] = None

    async def start(self):
        if self.is_running:
            logger.warning("Scheduler is already running.")
            return

        self.is_running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Ingestion scheduler started with interval {self.interval_sec}s.")

    async def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, RuntimeError):
                pass
            self._task = None
        logger.info("Ingestion scheduler stopped.")

    async def _run_loop(self):
        # Initial brief pause so application starts up cleanly
        await asyncio.sleep(2.0)
        while self.is_running:
            try:
                await self.trigger_cycle()
            except Exception as e:
                logger.error(f"Error in scheduler execution loop: {e}")

            try:
                await asyncio.sleep(self.interval_sec)
            except asyncio.CancelledError:
                break

    async def trigger_cycle(self) -> Dict[str, Any]:
        """
        Manually or periodically triggers a full ingestion cycle.
        """
        if self._lock.locked():
            logger.warning("Ingestion cycle already in progress. Skipping duplicate run.")
            return {"status": "SKIPPED", "reason": "Already running"}

        async with self._lock:
            t0 = datetime.now(timezone.utc).isoformat()
            summary = await ingestion_manager.run_full_ingestion_cycle()
            self.last_run_time = t0
            self.last_run_summary = summary
            return summary

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "interval_sec": self.interval_sec,
            "last_run_time": self.last_run_time,
            "last_run_summary": self.last_run_summary
        }

scheduler = IngestionScheduler(interval_sec=300)
