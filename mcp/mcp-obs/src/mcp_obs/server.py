import json
import os
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("mcp-obs")

_logs_url = ""
_traces_url = ""


class _LogsSearchQuery(BaseModel):
    query: str = Field(description="LogsQL query string (e.g., 'service.name:backend severity:ERROR')")
    limit: int = Field(default=100, description="Maximum number of log entries to return")


class _LogsErrorCountQuery(BaseModel):
    service: str = Field(description="Service name to filter (e.g., 'Learning Management Service')")
    minutes: int = Field(default=60, description="Time window in minutes")


class _TracesListQuery(BaseModel):
    service: str = Field(description="Service name to filter traces")
    limit: int = Field(default=20, description="Maximum number of traces to return")


class _TracesGetQuery(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


def _text(data: BaseModel | Sequence[BaseModel] | dict[str, Any] | str) -> list[TextContent]:
    if isinstance(data, BaseModel):
        payload: object = data.model_dump()
    elif isinstance(data, dict):
        payload = data
    elif isinstance(data, str):
        return [TextContent(type="text", text=data)]
    else:
        payload = [item.model_dump() if hasattr(item, "model_dump") else item for item in data]
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


async def _logs_search(args: _LogsSearchQuery) -> list[TextContent]:
    url = f"{_logs_url}/select/logsql/query"
    params = {"query": args.query, "limit": args.limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    results.append({"raw": line})
    return _text({"entries": results, "count": len(results)})


async def _logs_error_count(args: _LogsErrorCountQuery) -> list[TextContent]:
    time_window = f"{args.minutes}m"
    query = f'_time:{time_window} service.name:"{args.service}" severity:ERROR'
    url = f"{_logs_url}/select/logsql/query"
    params = {"query": query, "limit": 1000}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
        error_count = sum(1 for line in lines if line.strip())
    return _text({"service": args.service, "time_window_minutes": args.minutes, "error_count": error_count})


async def _traces_list(args: _TracesListQuery) -> list[TextContent]:
    url = f"{_traces_url}/select/jaeger/api/traces"
    params = {"service": args.service, "limit": args.limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
    traces = data.get("data", [])
    summary = [{"trace_id": t.get("traceID"), "span_count": len(t.get("spans", [])), "service_name": args.service} for t in traces]
    return _text({"traces": summary, "count": len(summary)})


async def _traces_get(args: _TracesGetQuery) -> list[TextContent]:
    url = f"{_traces_url}/select/jaeger/api/traces/{args.trace_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        data = response.json()
    return _text(data)


_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]
_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))


_register(
    "logs_search",
    "Search VictoriaLogs using LogsQL. Returns matching log entries.",
    _LogsSearchQuery,
    _logs_search,
)

_register(
    "logs_error_count",
    "Count error-level logs for a service over a time window.",
    _LogsErrorCountQuery,
    _logs_error_count,
)

_register(
    "traces_list",
    "List recent traces for a service from VictoriaTraces.",
    _TracesListQuery,
    _traces_list,
)

_register(
    "traces_get",
    "Fetch a specific trace by ID from VictoriaTraces.",
    _TracesGetQuery,
    _traces_get,
)


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


async def main() -> None:
    global _logs_url, _traces_url
    _logs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:9428").rstrip("/")
    _traces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:10428").rstrip("/")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)
