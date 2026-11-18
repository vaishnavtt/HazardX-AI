"""
HAZARDX AI — Alert Notification Service
Sends automated email notifications for HIGH (Orange) and SEVERE (Red) hazard alerts.
Features graceful fallback when SMTP credentials are not configured.
"""

import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, Optional
from ..config import settings
from ..schemas.alert import AlertItem
from ..services.data_storage_service import storage_service
from ..utils.logging_config import get_logger

logger = get_logger("notification_service")

SEVERITY_COLORS = {
    "RED": "#ef4444",
    "ORANGE": "#f97316",
    "YELLOW": "#eab308",
    "GREEN": "#10b981"
}

SEVERITY_MIN_ORDER = {
    "GREEN": 1,
    "YELLOW": 2,
    "ORANGE": 3,
    "RED": 4
}

class NotificationService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.email_from = settings.ALERT_EMAIL_FROM
        self.email_recipients = [r.strip() for r in settings.ALERT_EMAIL_RECIPIENTS.split(",") if r.strip()]
        self.min_severity = settings.ALERT_EMAIL_MIN_SEVERITY.upper()

    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.email_recipients)

    def should_notify(self, severity: str) -> bool:
        min_rank = SEVERITY_MIN_ORDER.get(self.min_severity, 3)
        sev_rank = SEVERITY_MIN_ORDER.get(severity.upper(), 1)
        return sev_rank >= min_rank

    async def notify_alert(self, alert: AlertItem) -> Dict[str, Any]:
        """
        Dispatches email notification for an alert if severity criteria are met.
        Gracefully logs and returns diagnostic status if unconfigured.
        """
        if not self.should_notify(alert.severity):
            return {
                "status": "SKIPPED_THRESHOLD",
                "detail": f"Severity {alert.severity} below threshold {self.min_severity}"
            }

        if alert.notification_sent:
            return {
                "status": "SUPPRESSED_DEDUP",
                "detail": "Notification already delivered for this alert."
            }

        if not self.is_configured():
            logger.info(
                f"[NOTIFICATION NOT_CONFIGURED] Alert {alert.alert_id} ({alert.hazard_type.upper()} {alert.severity}) "
                f"triggered. SMTP not configured; skipping email dispatch."
            )
            storage_service.log_alert_notification_event(
                alert.alert_id,
                "NOT_CONFIGURED",
                "SMTP credentials not configured. Notification not dispatched (status: NOT_CONFIGURED)."
            )
            return {
                "status": "NOT_CONFIGURED",
                "detail": "SMTP settings not configured. Alert logged without email dispatch."
            }

        # Dispatch via async threadpool to prevent blocking the event loop
        loop = asyncio.get_running_loop()
        try:
            success = await loop.run_in_executor(None, self._send_email_sync, alert)
            if success:
                storage_service.mark_alert_notification_sent(alert.alert_id)
                storage_service.log_alert_notification_event(
                    alert.alert_id,
                    "SENT",
                    f"Email delivered to {len(self.email_recipients)} recipient(s): {', '.join(self.email_recipients)}"
                )
                logger.info(f"Successfully dispatched alert email for {alert.alert_id}")
                return {"status": "SENT", "detail": f"Delivered to {len(self.email_recipients)} recipient(s)"}
            else:
                storage_service.log_alert_notification_event(
                    alert.alert_id,
                    "FAILED",
                    "SMTP transport error during dispatch."
                )
                return {"status": "FAILED", "detail": "SMTP transport error"}
        except Exception as e:
            logger.error(f"Error sending notification for alert {alert.alert_id}: {e}")
            storage_service.log_alert_notification_event(
                alert.alert_id,
                "FAILED",
                f"SMTP exception during dispatch: {e}"
            )
            return {"status": "FAILED", "detail": str(e)}

    def _send_email_sync(self, alert: AlertItem) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"[HAZARDX AI - {alert.severity}] {alert.title}"
            msg["From"] = self.email_from
            msg["To"] = ", ".join(self.email_recipients)

            html_content = self._render_html_template(alert)
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=12.0) as server:
                if self.smtp_tls:
                    server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.email_from, self.email_recipients, msg.as_string())
            return True
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            return False

    def _render_html_template(self, alert: AlertItem) -> str:
        color = SEVERITY_COLORS.get(alert.severity, "#06b6d4")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #030712; color: #f3f4f6; padding: 24px; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: #0f172a; border-radius: 12px; border: 1px solid #1e293b; overflow: hidden; }}
            .header {{ background-color: #020617; padding: 20px 24px; border-bottom: 2px solid {color}; }}
            .badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; background-color: {color}; color: #ffffff; text-transform: uppercase; }}
            .body {{ padding: 24px; }}
            .title {{ font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 12px; margin-bottom: 8px; }}
            .meta {{ font-size: 12px; color: #94a3b8; font-family: monospace; margin-bottom: 16px; }}
            .card {{ background-color: #1e293b; padding: 16px; border-radius: 8px; margin-bottom: 16px; border-left: 4px solid {color}; }}
            .guidance {{ background-color: #1e1b4b; border: 1px solid #3730a3; padding: 14px; border-radius: 8px; font-size: 13px; color: #c7d2fe; margin-bottom: 20px; }}
            .footer {{ background-color: #020617; padding: 16px 24px; font-size: 11px; color: #64748b; border-top: 1px solid #1e293b; }}
            .btn {{ display: inline-block; background-color: #0284c7; color: #ffffff; text-decoration: none; padding: 10px 18px; border-radius: 6px; font-size: 13px; font-weight: bold; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <span class="badge">{alert.severity} ALERT</span>
              <div style="float: right; color: #64748b; font-size: 11px; font-family: monospace;">HAZARDX AI TELEMETRY</div>
              <div class="title">{alert.title}</div>
              <div class="meta">
                Coordinates: {alert.latitude:.4f}°, {alert.longitude:.4f}° | Hazard: {alert.hazard_type.upper()} | Time: {alert.created_at} UTC
              </div>
            </div>
            <div class="body">
              <div class="card">
                <div style="font-size: 13px; line-height: 1.6; color: #e2e8f0;">
                  {alert.description}
                </div>
              </div>
              <div class="guidance">
                <strong>Decision Support Guidance:</strong><br>
                {alert.guidance}
              </div>
              <div style="text-align: center; margin: 24px 0 12px 0;">
                <a href="http://127.0.0.1:5173/alerts?id={alert.alert_id}" class="btn">View Live in HAZARDX Alert Center</a>
              </div>
            </div>
            <div class="footer">
              <strong>Source:</strong> {alert.source}<br>
              <strong>Disclaimer:</strong> {alert.disclaimer}
            </div>
          </div>
        </body>
        </html>
        """

notification_service = NotificationService()

