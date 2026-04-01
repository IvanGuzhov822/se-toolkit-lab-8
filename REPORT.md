# Lab 8 — Report

## Task 1A — Bare agent

### Setup Steps

1. Initialized nanobot project:
   ```bash
   uv init nanobot
   cd nanobot
   uv add "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"
   ```

2. Ran onboard wizard:
   ```bash
   uv run nanobot onboard -c config.json
   ```

3. Configured `config.json`:
   - `agents.defaults.workspace`: `./workspace`
   - `agents.defaults.model`: `coder-model`
   - `agents.defaults.provider`: `custom`
   - `providers.custom.apiKey`: `yachta-barakuda`
   - `providers.custom.apiBase`: `http://localhost:42005/v1`

### Agent Responses

**Test 1: "What is the agentic loop?"**

Command:
```bash
cd nanobot && uv run nanobot agent --logs --session cli:task1a-loop -c ./config.json -m "What is the agentic loop?"
```

Response:
```
The agentic loop is the fundamental reasoning cycle that autonomous AI agents follow to accomplish tasks:

Perceive → Reason → Act → Observe → Reflect → (repeat)

Stage     What Happens
────────────────────────────────────────────────────────────────────────────────
Perceive  Gather input from user, tools, and environment
Reason    Analyze information and plan next actions
Act       Execute actions using available tools
Observe   Receive feedback from those actions
Reflect   Evaluate progress toward goals; decide to continue or stop

This loop enables agents to work autonomously on multi-step tasks, adapt to unexpected outcomes, and iteratively refine their approach until a goal is achieved.
```

**Checkpoint Status: PASS**

---

## Task 1B — Agent with LMS tools

### Setup Steps

1. Added MCP server as dependency:
   ```bash
   cd nanobot
   uv add mcp-lms --editable ../mcp/mcp-lms
   ```

2. Added MCP configuration to `nanobot/config.json` with environment variables for backend URL and API key.

### Agent Responses

**Test 1: "What labs are available?"**

Command:
```bash
cd nanobot && NANOBOT_LMS_BACKEND_URL=http://localhost:42002 NANOBOT_LMS_API_KEY=genaker-barakuda uv run nanobot agent --logs --session cli:task1b-labs -c ./config.json -m "What labs are available?"
```

Response:
```
The LMS sync completed successfully (336 new records fetched). Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08
```

**Checkpoint Status: PASS**

---

## Task 1C — Skill prompt

### Skill File Created

`nanobot/workspace/skills/lms/SKILL.md` — teaches the agent to ask for lab selection when the user query is ambiguous.

### Agent Response

**Test: "Show me the scores"**

Command:
```bash
cd nanobot && NANOBOT_LMS_BACKEND_URL=http://localhost:42002 NANOBOT_LMS_API_KEY=genaker-barakuda uv run nanobot agent --logs --session cli:task1c-v2 -c ./config.json -m "Show me the scores"
```

Response:
```
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08

Which lab would you like to see the scores for?
```

**Checkpoint Status: PASS** — Agent asks for lab selection when query is ambiguous.

---

## Summary of Files

| File | Purpose |
|------|---------|
| `nanobot/pyproject.toml` | Project dependencies (nanobot-ai, mcp-lms, nanobot-webchat, mcp-webchat) |
| `nanobot/config.json` | Agent configuration with custom provider, MCP servers, and webchat channel |
| `nanobot/workspace/skills/lms/SKILL.md` | LMS skill prompt for tool usage strategy |
| `nanobot/entrypoint.py` | Docker entrypoint that resolves env vars and starts nanobot gateway |
| `nanobot/Dockerfile` | Multi-stage Docker build for nanobot |
| `docker-compose.yml` | Nanobot and client-web-flutter services |
| `caddy/Caddyfile` | Routes for /ws/chat and /flutter |

---

## Task 2A — Deployed agent

### Startup Log Excerpt

```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
MCP server 'lms': connected, 9 tools registered
MCP server 'webchat': connected, 1 tools registered
Agent loop started
```

**Checkpoint Status: PASS** — nanobot gateway is running with webchat channel and MCP tools.

---

## Task 2B — Web client

### WebSocket Test

Command:
```bash
uv run python -c "
import asyncio, json, websockets
async def main():
    uri = 'ws://localhost:42002/ws/chat?access_key=staksel-barakuda'
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({'content': 'What labs are available?'}))
        print(await ws.recv())
asyncio.run(main())
"
```

Response:
```json
{
  "type": "text",
  "content": "Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy\n4. **Lab 04** — Testing, Front-end, and AI Agents\n5. **Lab 05** — Data Pipeline and Analytics Dashboard\n6. **Lab 06** — Build Your Own Agent\n7. **Lab 07** — Build a Client with an AI Coding Agent\n8. **lab-08**\n\nWould you like to see details for any specific lab, such as pass rates, completion rates, group performance, or top learners?",
  "format": "markdown"
}
```

### Flutter Client

The Flutter web client is accessible at `http://localhost:42002/flutter/`. It serves the login screen and accepts the `NANOBOT_ACCESS_KEY` for authentication.

**Checkpoint Status: PASS** — WebSocket endpoint responds with real backend data and Flutter client serves content.
=======
