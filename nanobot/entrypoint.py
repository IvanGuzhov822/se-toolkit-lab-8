#!/usr/bin/env python3
import json
import os
from pathlib import Path


def main():
    config_path = Path("/app/nanobot/config.json")
    workspace_path = Path("/app/nanobot/workspace")
    resolved_path = Path("/tmp/nanobot/config.resolved.json")

    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path) as f:
        config = json.load(f)

    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key

    if llm_api_base_url := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base_url

    if llm_api_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_api_model

    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        if "webchat" not in config["channels"]:
            config["channels"]["webchat"] = {}
        config["channels"]["webchat"]["host"] = webchat_host

    if webchat_port := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT"):
        if "webchat" not in config["channels"]:
            config["channels"]["webchat"] = {}
        config["channels"]["webchat"]["port"] = int(webchat_port)

    if lms_backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url

    if lms_api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    if webchat_ui_relay_url := os.environ.get("NANOBOT_UI_RELAY_URL"):
        if "webchat" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["webchat"] = {}
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_UI_RELAY_URL"] = webchat_ui_relay_url

    if webchat_ui_token := os.environ.get("NANOBOT_UI_RELAY_TOKEN"):
        if "webchat" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["webchat"] = {}
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_UI_RELAY_TOKEN"] = webchat_ui_token

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}")

    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_path), "--workspace", str(workspace_path)])


if __name__ == "__main__":
    main()
