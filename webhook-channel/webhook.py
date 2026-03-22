#!/usr/bin/env python3
import asyncio
import threading
import argparse
from contextlib import asynccontextmanager
import os
from pathlib import Path
from dotenv import load_dotenv
if claude_dir := os.environ.get("CLAUDE_PROJECT_DIR"):
    load_dotenv(Path(claude_dir) / ".env")
load_dotenv()  # 로컬 .env fallback

import logging
logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(name)s: %(message)s")
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

import anyio
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route, Mount

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage, JSONRPCNotification, Tool, TextContent

from channels import get_sender, get_background_tasks
from channels.utils import make_event

PORT = 8788
queue: asyncio.Queue = asyncio.Queue()
_sender = get_sender()
_loop: asyncio.AbstractEventLoop

mcp = Server(
    name="webhook",
    version="0.0.1",
    instructions='Messages arrive as <channel source="webhook" chat_id="...">. Reply with the reply tool, passing the chat_id from the tag.',
)

sse = SseServerTransport("/messages/")


# --- MCP Tools ---

@mcp.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="reply",
        description="Send a message back over this channel",
        inputSchema={
            "type": "object",
            "properties": {
                "chat_id": {"type": "string", "description": "The conversation to reply in"},
                "text": {"type": "string", "description": "The message to send"},
            },
            "required": ["chat_id", "text"],
        },
    )]


@mcp.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "reply":
        await _sender.send(arguments["chat_id"], arguments["text"])
        return [TextContent(type="text", text="sent")]
    raise ValueError(f"unknown tool: {name}")


# --- MCP init ---

def mcp_init_options():
    return InitializationOptions(
        server_name="webhook",
        server_version="0.0.1",
        capabilities=mcp.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={"claude/channel": {}},
        ),
    )


async def notification_sender(write_stream):
    while True:
        event = await queue.get()
        try:
            notification = JSONRPCNotification(
                jsonrpc="2.0",
                method="notifications/claude/channel",
                params={"content": event["content"], "meta": event["meta"]},
            )
            await write_stream.send(SessionMessage(JSONRPCMessage(notification)))
        except anyio.ClosedResourceError:
            queue.put_nowait(event)
            break


# --- stdio mode ---

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(length)
        _loop.call_soon_threadsafe(queue.put_nowait, make_event(body_bytes.decode(), self.path))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args): pass


async def run_stdio():
    global _loop
    _loop = asyncio.get_running_loop()

    http = HTTPServer(("127.0.0.1", PORT), WebhookHandler)
    threading.Thread(target=http.serve_forever, daemon=True).start()

    async with stdio_server() as (read_stream, write_stream):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(notification_sender(write_stream))
            tg.create_task(mcp.run(read_stream, write_stream, mcp_init_options()))
            for coro in get_background_tasks(queue):
                tg.create_task(coro)


# --- SSE mode ---

async def handle_sse(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(notification_sender(write_stream))
            tg.create_task(mcp.run(read_stream, write_stream, mcp_init_options()))


async def handle_webhook(request: Request):
    body = (await request.body()).decode()
    await queue.put(make_event(body, request.url.path))
    return Response("ok")


@asynccontextmanager
async def lifespan(app):
    tasks = [asyncio.create_task(coro) for coro in get_background_tasks(queue)]
    yield
    for task in tasks:
        task.cancel()


def run_sse():
    routes = [
        Route("/sse", handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
        Route("/", handle_webhook, methods=["POST"]),
    ]
    uvicorn.run(Starlette(routes=routes, lifespan=lifespan), host="127.0.0.1", port=PORT)


# --- Entry point ---

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    args = parser.parse_args()

    if args.transport == "sse":
        run_sse()
    else:
        asyncio.run(run_stdio())


if __name__ == "__main__":
    run()
