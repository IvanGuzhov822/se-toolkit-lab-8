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
| `nanobot/pyproject.toml` | Project dependencies (nanobot-ai, mcp-lms) |
| `nanobot/config.json` | Agent configuration with custom provider and MCP server |
| `nanobot/workspace/skills/lms/SKILL.md` | LMS skill prompt for tool usage strategy |
