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
   - `providers.custom.apiKey`: `qwen-code-api-key-secret`
   - `providers.custom.apiBase`: `http://localhost:42005/v1`

### Files Created/Modified

- `nanobot/pyproject.toml` — nanobot-ai dependency
- `nanobot/config.json` — agent configuration with custom Qwen Code provider
- `nanobot/workspace/` — agent workspace directory with default skills

### Agent Responses

**Note:** Full agent testing requires the Qwen Code API and LMS backend to be running on the VM. The commands below should be executed on the VM after starting all services.

Test command for "What is the agentic loop?":
```bash
cd nanobot && uv run nanobot agent --logs --session cli:task1a-loop -c ./config.json -m "What is the agentic loop?"
```

Expected response: The agent should explain that the agentic loop is the cycle of:
1. Receiving a user message
2. Sending it to the LLM with available tools
3. Parsing tool calls from the LLM response
4. Executing the tools
5. Feeding results back to the LLM
6. Repeating until the task is complete

Test command for "What labs are available?":
```bash
cd nanobot && uv run nanobot agent --logs --session cli:task1a-labs -c ./config.json -m "What labs are available in our LMS?"
```

Expected response at this stage: The agent should NOT return real backend data yet. It may say it doesn't know or inspect local repo files, but it cannot query the live LMS until Part B adds the MCP server.

---

## Task 1B — Agent with LMS tools

### Setup Steps

1. Added MCP server as dependency:
   ```bash
   cd nanobot
   uv add mcp-lms --editable ../mcp/mcp-lms
   ```

2. Added MCP configuration to `nanobot/config.json`:
   ```json
   {
     "tools": {
       "mcpServers": {
         "lms": {
           "command": "python",
           "args": ["-m", "mcp_lms"],
           "env": {
             "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
             "NANOBOT_LMS_API_KEY": "lms-api-key-secret"
           }
         }
       }
     }
   }
   ```

### Files Modified

- `nanobot/pyproject.toml` — added mcp-lms workspace dependency
- `nanobot/config.json` — added MCP server configuration

### Available MCP Tools

- `lms_health` — Check backend health
- `lms_labs` — List all labs
- `lms_learners` — List all learners
- `lms_pass_rates` — Get pass rates for a lab
- `lms_timeline` — Get submission timeline for a lab
- `lms_groups` — Get group performance for a lab
- `lms_top_learners` — Get top learners for a lab
- `lms_completion_rate` — Get completion rate for a lab
- `lms_sync_pipeline` — Trigger sync pipeline

### Agent Responses

Test command for "What labs are available?":
```bash
cd nanobot && NANOBOT_LMS_BACKEND_URL=http://localhost:42002 NANOBOT_LMS_API_KEY=lms-api-key-secret uv run nanobot agent --logs --session cli:task1b-labs -c ./config.json -m "What labs are available?"
```

Expected response: The agent should call `lms_labs` and return real lab names from the backend (e.g., `lab-01`, `lab-02`, etc.).

Test command for "Is the LMS backend healthy?":
```bash
cd nanobot && NANOBOT_LMS_BACKEND_URL=http://localhost:42002 NANOBOT_LMS_API_KEY=lms-api-key-secret uv run nanobot agent --logs --session cli:task1b-health -c ./config.json -m "Is the LMS backend healthy?"
```

Expected response: The agent should call `lms_health` and report the backend status with item count.

---

## Task 1C — Skill prompt

### Skill File Created

`nanobot/workspace/skills/lms/SKILL.md`:

```markdown
---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to access live course data from the LMS backend.

## Available Tools

- `lms_health` - Check if the LMS backend is healthy and report the item count
- `lms_labs` - List all labs available in the LMS
- `lms_learners` - List all learners registered in the LMS
- `lms_pass_rates` - Get pass rates for a specific lab (requires lab parameter)
- `lms_timeline` - Get submission timeline for a specific lab (requires lab parameter)
- `lms_groups` - Get group performance for a specific lab (requires lab parameter)
- `lms_top_learners` - Get top learners by average score for a specific lab (requires lab parameter)
- `lms_completion_rate` - Get completion rate for a specific lab (requires lab parameter)
- `lms_sync_pipeline` - Trigger the LMS sync pipeline

## Strategy

### When user asks about labs, scores, pass rates, completion, groups, timeline, or top learners:

1. If the user did not specify a lab identifier:
   - Call `lms_labs` first to get the list of available labs
   - Use `mcp_webchat_ui_message` with `type: "choice"` to let the user select a lab
   - Provide each lab's `id` as the value and `title` as the label
   - If UI choice is not available on the channel, ask in plain text which lab they want

2. If the user specified a lab:
   - Call the appropriate tool directly with the lab identifier

### When user asks "what can you do?":

Explain that you can:
- Check LMS backend health
- List available labs and learners
- Show pass rates, completion rates, timelines, and group performance for specific labs
- Identify top learners per lab
- Trigger the LMS sync pipeline

### Response formatting:

- Format percentages with the % symbol
- Format counts as plain numbers
- Keep responses concise
- Include relevant lab titles when presenting results

### Error handling:

- If a tool fails, explain the error clearly and suggest retrying or checking backend health
- If no labs are available, suggest triggering the sync pipeline first
```

### Agent Response

Test command for "Show me the scores":
```bash
cd nanobot && NANOBOT_LMS_BACKEND_URL=http://localhost:42002 NANOBOT_LMS_API_KEY=lms-api-key-secret uv run nanobot agent --logs --session cli:task1c -c ./config.json -m "Show me the scores"
```

Expected response: The agent should ask which lab the user wants to see scores for, or list available labs first using `lms_labs` and then present a choice.

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
