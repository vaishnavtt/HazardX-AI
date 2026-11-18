"""
HAZARDX AI — Background Alert Monitoring Worker
Asynchronously polls cached data feeds, applies rate-limiting backoffs,
executes alert generation cycles, and provides monitoring health telemetry.
"""

import time
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from .alert_engine import alert_engine
from ..schemas.alert import MonitorStatusResponse
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("alert_monitor")

class AlertMonitor:
    def __init__(self):
        self.interval_seconds = getattr(settings, "ALERT_MONITOR_INTERVAL_SECONDS", 180)
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

        # Telemetry metrics
        self.total_cycles = 0
        self.total_alerts_generated = 0
        self.last_run_time: Optional[str] = None
        self.next_run_time: Optional[str] = None
        self.last_duration_ms: Optional[float] = None
        self.last_error: Optional[str] = None

    def start(self) -> None:
        """Starts the background monitoring loop as an async task."""
        if self.is_running:
            logger.warning("Alert monitor is already running.")
            return

        self.is_running = True
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Alert monitor started with {self.interval_seconds}s polling cadence.")

    async def stop(self) -> None:
        """Gracefully shuts down the background monitoring worker."""
        if not self.is_running:
            return

        logger.info("Stopping alert monitor background task...")
        self.is_running = False
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, RuntimeError):
                pass
            self._task = None
        logger.info("Alert monitor successfully stopped.")

    async def trigger_cycle(self) -> Dict[str, Any]:
        """Executes a single monitoring cycle synchronously/on-demand."""
        t0 = time.time()
        self.last_run_time = datetime.now(timezone.utc).isoformat()
        try:
            alerts = await alert_engine.evaluate_live_streams()
            dur_ms = (time.time() - t0) * 1000
            self.total_cycles += 1
            self.total_alerts_generated += len(alerts)
            self.last_duration_ms = round(dur_ms, 1)
            self.last_error = None
            logger.info(f"Completed alert monitoring cycle #{self.total_cycles} in {dur_ms:.1f}ms: generated {len(alerts)} alert(s)")
            return {
                "success": True,
                "cycle": self.total_cycles,
                "duration_ms": self.last_duration_ms,
                "alerts_evaluated": len(alerts)
            }
        except Exception as e:
            dur_ms = (time.time() - t0) * 1000
            self.last_duration_ms = round(dur_ms, 1)
            self.last_error = str(e)
            logger.error(f"Error in alert monitoring cycle: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "duration_ms": self.last_duration_ms
            }

    async def _run_loop(self) -> None:
        # Initial brief delay to allow backend to finish startup
        await asyncio.sleep(5)
        
        while self.is_running and not self._stop_event.is_set():
            next_ts = time.time() + self.interval_seconds
            self.next_run_time = datetime.fromtimestamp(next_ts, timezone.utc).isoformat()
            
            await self.trigger_cycle()

            try:
                # Sleep until next interval or until stop event is signaled
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval_seconds)
            except asyncio.TimeoutError:
                pass

    def get_status(self) -> MonitorStatusResponse:
        return MonitorStatusResponse(
            is_running=self.is_running,
            interval_seconds=self.interval_seconds,
            last_run_timestamp=self.last_run_time,
            next_run_timestamp=self.next_run_time,
            total_cycles_completed=self.total_cycles,
            total_alerts_generated=self.total_alerts_generated,
            total_alerts_updated=0,
            last_cycle_duration_ms=self.last_duration_ms,
            last_error=self.last_error
        )

alert_monitor = AlertMonitor()

