"""MCP server for reading and posting Slack messages via Bot Token."""

import json
import os
from pathlib import Path
from mcp.server import FastMCP
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

server = FastMCP("mcp-slack")


def _load_token() -> str:
    """Load SLACK_BOT_TOKEN from environment or .env file."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if token:
        return token

    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("SLACK_BOT_TOKEN="):
                return line.split("=", 1)[1].strip().strip("\"'")

    raise RuntimeError("SLACK_BOT_TOKEN not found in environment or .env file")


SLACK_BOT_TOKEN = _load_token()

client = WebClient(token=SLACK_BOT_TOKEN)


@server.tool()
def slack_post(channel: str, message: str) -> str:
    """Post a message to a Slack channel. Channel can be a name (e.g. 'general') or a channel ID."""
    try:
        resolved = channel if _is_channel_id(channel) else f"#{channel.lstrip('#')}"
        result = client.chat_postMessage(channel=resolved, text=message)
        return json.dumps({"ok": True, "ts": result["ts"], "channel": result["channel"]})
    except SlackApiError as e:
        return json.dumps({"error": e.response["error"]})


@server.tool()
def slack_read(channel: str, limit: int = 20) -> str:
    """Read recent messages from a Slack channel. Channel can be a name or a channel ID."""
    try:
        result = client.conversations_history(
            channel=channel if _is_channel_id(channel) else _resolve_channel_id(channel),
            limit=limit,
        )
        messages = [
            {"user": m.get("user"), "text": m.get("text"), "ts": m.get("ts")}
            for m in result["messages"]
        ]
        return json.dumps(messages)
    except SlackApiError as e:
        return json.dumps({"error": e.response["error"]})


@server.tool()
def slack_list_channels(member_only: bool = False) -> str:
    """List Slack channels. Set member_only=True to only show channels the bot is in (can read/post)."""
    try:
        result = client.conversations_list(types="public_channel,private_channel")
        channels = [
            {"id": c["id"], "name": c["name"], "is_private": c["is_private"], "is_member": c.get("is_member", False)}
            for c in result["channels"]
            if not member_only or c.get("is_member", False)
        ]
        return json.dumps(channels)
    except SlackApiError as e:
        return json.dumps({"error": e.response["error"]})


def _is_channel_id(value: str) -> bool:
    """Slack channel IDs start with C (public), D (DM), or G (private/group)."""
    return len(value) > 1 and value[0] in ("C", "D", "G") and value[1:].isupper()


def _resolve_channel_id(channel_name: str) -> str:
    """Resolve a channel name to its Slack channel ID."""
    result = client.conversations_list(types="public_channel,private_channel")
    for c in result["channels"]:
        if c["name"] == channel_name.lstrip("#"):
            return c["id"]
    raise ValueError(f"Channel '{channel_name}' not found")


if __name__ == "__main__":
    server.run(transport="stdio")
