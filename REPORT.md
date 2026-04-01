# Lab 8 — Report

## Task 1A — Bare agent

**Response:** "The agentic loop is the fundamental reasoning cycle: Perceive → Reason → Act → Observe → Reflect"

**Checkpoint Status: PASS**

---

## Task 1B — Agent with LMS tools

**Response:** "Here are the available labs: Lab 01, Lab 02, Lab 03, Lab 04, Lab 05, Lab 06, Lab 07, lab-08"

**Checkpoint Status: PASS**

---

## Task 1C — Skill prompt

**Response:** Agent asks "Which lab would you like to see the scores for?" instead of dumping all data.

**Checkpoint Status: PASS**

---

## Task 2A — Deployed agent

**Startup Log:**
```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
MCP server 'lms': connected, 9 tools registered
MCP server 'webchat': connected, 1 tools registered
MCP server 'obs': connected, 4 tools registered
Agent loop started
```

**Checkpoint Status: PASS**

---

## Task 2B — Web client

**WebSocket Response:**
```json
{"type":"text","content":"Here are the available labs: Lab 01, Lab 02, Lab 03, Lab 04, Lab 05, Lab 06, Lab 07, lab-08"}
```

**Flutter Client:** Accessible at `http://localhost:42002/flutter/`

**Checkpoint Status: PASS**

---

## Task 3A — Structured logging

**Structured Log Entry (JSON format):**
```json
{
  "timestamp": "2026-04-01 09:19:34,871",
  "level": "INFO",
  "service": "lms_backend.main",
  "event": "request_started",
  "trace_id": "c02aa9a8dbd2161da0602ae54e579094",
  "span_id": "423076fce6978867",
  "resource.service.name": "Learning Management Service",
  "trace_sampled": true
}
```

**Log Flow for Single Request:**
```
trace_id=c02aa9a8dbd2161da0602ae54e579094 span_id=423076fce6978867 - request_started
trace_id=c02aa9a8dbd2161da0602ae54e579094 span_id=423076fce6978867 - auth_success
trace_id=c02aa9a8dbd2161da0602ae54e579094 span_id=423076fce6978867 - db_query
trace_id=c02aa9a8dbd2161da0602ae54e579094 span_id=423076fce6978867 - request_completed
```

**Checkpoint Status: PASS**

---

## Task 3B — Traces

**Trace Data from VictoriaTraces API:**
```json
{
  "data": [{
    "traceID": "c02aa9a8dbd2161da0602ae54e579094",
    "spans": [
      {
        "operationName": "GET /items/",
        "spanID": "423076fce6978867",
        "duration": 65238,
        "tags": [
          {"key": "http.method", "value": "GET"},
          {"key": "http.status_code", "value": "200"},
          {"key": "span.kind", "value": "server"}
        ]
      },
      {
        "operationName": "SELECT db-lab-8",
        "spanID": "9ac214fa562e88ca",
        "duration": 45623,
        "tags": [
          {"key": "db.system", "value": "postgresql"},
          {"key": "db.name", "value": "db-lab-8"},
          {"key": "span.kind", "value": "client"}
        ]
      },
      {
        "operationName": "connect",
        "spanID": "b6277aa75a569c5c",
        "duration": 216,
        "tags": [
          {"key": "db.system", "value": "postgresql"},
          {"key": "net.peer.name", "value": "postgres"}
        ]
      }
    ]
  }]
}
```

**Span Hierarchy:**
- GET /items/ (65ms) - root span
  - SELECT db-lab-8 (45ms) - database query
  - connect (0.2ms) - database connection
  - GET /items/ http send (0.16ms) - response

**Checkpoint Status: PASS**

---

## Task 3C — Observability MCP tools

**MCP Tools Registered:**
- `mcp_obs_logs_search` — Search VictoriaLogs using LogsQL
- `mcp_obs_logs_error_count` — Count errors for a service
- `mcp_obs_traces_list` — List recent traces for a service
- `mcp_obs_traces_get` — Fetch specific trace by ID

**Agent Tool Call:**
```
Tool call: mcp_obs_logs_error_count({"service": "Learning Management Service", "minutes": 10})
```

**Tool Output:**
```json
{"service": "Learning Management Service", "time_window_minutes": 10, "error_count": 0}
```

**Agent Response:**
```
Good news! There are **0 errors** in the Learning Management Service over the last 10 minutes. 
The LMS backend appears to be healthy.
```

**Files Created:**
- `mcp/mcp-obs/src/mcp_obs/server.py`
- `mcp/mcp-obs/src/mcp_obs/__main__.py`
- `mcp/mcp-obs/pyproject.toml`
- `nanobot/workspace/skills/observability/SKILL.md`

**Checkpoint Status: PASS**
