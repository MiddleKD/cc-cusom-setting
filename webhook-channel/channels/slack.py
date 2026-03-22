import asyncio
import os
from slack_sdk.webhook.async_client import AsyncWebhookClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from . import ChannelSender
from .utils import make_event


class SlackChannel(ChannelSender):

    # --- 송신 (SLACK_WEBHOOK_URL) ---

    def __init__(self):
        self._client = AsyncWebhookClient(os.environ["SLACK_WEBHOOK_URL"])

    @classmethod
    def is_available(cls) -> bool:
        return bool(os.environ.get("SLACK_WEBHOOK_URL"))

    async def send(self, chat_id: str, text: str) -> None:
        await self._client.send(text=text)

    # --- 수신 (SLACK_APP_TOKEN) ---

    @classmethod
    def is_receiving_available(cls) -> bool:
        return bool(os.environ.get("SLACK_APP_TOKEN"))

    @classmethod
    async def start_socket_mode(cls, queue: asyncio.Queue) -> None:
        client = SocketModeClient(app_token=os.environ["SLACK_APP_TOKEN"])

        async def handler(client: SocketModeClient, req: SocketModeRequest):
            if req.type == "events_api":
                event = req.payload.get("event", {})
                if (
                    event.get("type") == "message"
                    and not event.get("bot_id")
                    and not event.get("subtype")
                ):
                    await queue.put(make_event(event.get("text", ""), "/slack"))
            await client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id)
            )

        client.socket_mode_request_listeners.append(handler)
        await client.connect()
        await asyncio.sleep(float("inf"))
