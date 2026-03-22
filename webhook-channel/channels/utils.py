import uuid


def make_event(body: str, path: str) -> dict:
    return {"content": body, "meta": {"chat_id": uuid.uuid4().hex, "path": path, "method": "POST"}}
