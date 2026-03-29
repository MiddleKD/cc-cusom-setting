import asyncio
import json
import logging
import os

import httpx

from . import ChannelSender
from .utils import make_event

logger = logging.getLogger(__name__)


class ChorusChannel(ChannelSender):

    # --- 송신 (no-op: Claude가 chorus MCP 도구를 통해 직접 처리) ---

    def __init__(self):
        pass

    @classmethod
    def is_available(cls) -> bool:
        return bool(os.environ.get("CHORUS_API_KEY"))

    async def send(self, chat_id: str, text: str) -> None:  # noqa: ARG002
        pass

    # --- 수신 (CHORUS_API_URL + CHORUS_API_KEY) ---

    @classmethod
    def is_receiving_available(cls) -> bool:
        return bool(os.environ.get("CHORUS_API_URL")) and bool(
            os.environ.get("CHORUS_API_KEY")
        )

    @classmethod
    async def start_socket_mode(cls, queue: asyncio.Queue) -> None:
        url = os.environ["CHORUS_API_URL"].rstrip("/") + "/api/events/notifications"
        headers = {
            "Authorization": f"Bearer {os.environ['CHORUS_API_KEY']}",
            "Accept": "text/event-stream",
        }

        while True:
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream("GET", url, headers=headers) as response:
                        response.raise_for_status()
                        logger.info("Chorus SSE connected.")
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                            if line.startswith(":"):
                                # `: connected` 또는 `: heartbeat` 코멘트 — 무시
                                continue
                            if line.startswith("data:"):
                                raw = line[len("data:"):].strip()
                                try:
                                    payload = json.loads(raw)
                                except json.JSONDecodeError:
                                    logger.warning("Chorus SSE: JSON 파싱 실패: %s", raw)
                                    continue
                                if payload.get("type") == "new_notification":
                                    notification_uuid = payload.get("notificationUuid", "")
                                    unread = payload.get("unreadCount", "")
                                    body = (
                                        f"You have a new Chorus notification (uuid: {notification_uuid}, unread: {unread}). "
                                        f"Call chorus_get_notifications() to see what work has been assigned to you, "
                                        f"then proceed with the task immediately."
                                    )
                                    await queue.put(
                                        make_event(body, "/chorus/notifications")
                                    )
            except Exception as exc:
                logger.error("Chorus SSE 연결 오류: %s — 5초 후 재연결 시도.", exc)
            await asyncio.sleep(5)
