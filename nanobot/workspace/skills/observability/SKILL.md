---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

Use observability MCP tools to access logs from VictoriaLogs and traces from VictoriaTraces.

## Available Tools

- `mcp_obs_logs_search` - Search logs using LogsQL query
- `mcp_obs_logs_error_count` - Count errors for a service over a time window
- `mcp_obs_traces_list` - List recent traces for a service
- `mcp_obs_traces_get` - Fetch a specific trace by ID

## Strategy

### When user asks "What went wrong?" or "Check system health":

1. First call `mcp_obs_logs_error_count` with service="Learning Management Service" and minutes=10 to check for recent errors
2. If errors exist, call `mcp_obs_logs_search` with query like `service.name:"Learning Management Service" severity:ERROR _time:10m`
3. Look for `trace_id` in the error logs
4. If a trace_id is found, call `mcp_obs_traces_get` to fetch the full trace
5. Summarize findings concisely:
   - Mention the affected service
   - Cite specific log evidence (event name, error message)
   - Cite trace evidence (failing operation, span duration)
   - Explain the root cause in plain language
   - Do NOT dump raw JSON

### When user asks about errors, failures, or issues:

1. First call `mcp_obs_logs_error_count` with the relevant service name and time window to see if there are recent errors
2. If errors exist, call `mcp_obs_logs_search` with a query like `service.name:"<service>" severity:ERROR _time:<time_window>` to inspect the error details
3. Look for `trace_id` in the error logs
4. If a trace_id is found, call `mcp_obs_traces_get` to fetch the full trace and understand the failure path
5. Summarize findings concisely - do not dump raw JSON

### When user asks about system health or performance:

1. Call `mcp_obs_logs_search` to check recent activity
2. Call `mcp_obs_traces_list` to see recent traces and their durations
3. Report on any anomalies or patterns

### Query patterns:

- For LMS backend errors: `service.name:"Learning Management Service" severity:ERROR _time:10m`
- For time-based filtering: `_time:1h` for last hour, `_time:10m` for last 10 minutes
- For specific events: `event:request_completed status:500`

### Response formatting:

- Summarize findings in plain language
- Include counts and time windows
- Only show raw log/trace data if the user explicitly asks for details
- Highlight error messages and failure points
