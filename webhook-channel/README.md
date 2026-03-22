# webhook-channel

Slack DM → Claude Code 채널 MCP 서버.

## 환경변수

`~/.claude/.env` 또는 프로젝트 `.env`에 작성:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/...   # Claude → Slack 송신
SLACK_APP_TOKEN=xapp-...                         # Slack → Claude 수신 (Socket Mode)
```

## 실행

### SSE 모드 (수동 실행)

```bash
uvx --no-cache --from /path/to/webhook-channel webhook --transport sse
```

`.mcp.json`:
```json
"webhook": { "type": "sse", "url": "http://127.0.0.1:8788/sse" }
```

### stdio 모드 (Claude Code가 자동 실행 — 권장)

`.mcp.json`:
```json
"webhook": {
  "type": "stdio",
  "command": "uvx",
  "args": ["--no-cache", "--from", "/path/to/webhook-channel", "webhook"]
}
```

## Slack 앱 설정

- **Socket Mode** 활성화 (`Settings > Socket Mode`)
- App Token 스코프: `connections:write`
- Event Subscriptions: `message.im` 구독
- 봇을 DM에 초대
