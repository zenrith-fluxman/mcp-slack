# mcp-slack

MCP server for reading and posting Slack messages. Gives Claude Code (or any MCP client) the ability to list channels, read messages, and post to any channel in a Slack workspace.

## Tools

| Tool | Description |
|------|-------------|
| `slack_post` | Post a message to a channel |
| `slack_read` | Read recent messages from a channel |
| `slack_list_channels` | List all channels (optionally filter to joined only) |

## Prerequisites

1. A Slack workspace
2. A Slack App with a Bot Token (`xoxb-...`). Create one at [api.slack.com/apps](https://api.slack.com/apps)
3. Bot Token Scopes (add under OAuth & Permissions, then reinstall the app):
   - `chat:write`
   - `channels:read`
   - `channels:history`
   - `groups:read`
   - `groups:history`
   - `im:read` (optional, for DMs)
   - `im:write` (optional, for DMs)
   - `im:history` (optional, for DMs)
4. Invite the bot to channels you want it to access: `/invite @YourBot`

## Setup

```bash
git clone https://github.com/zenrith-fluxman/mcp-slack.git
cd mcp-slack
python -m venv .venv
source .venv/bin/activate
pip install slack_sdk mcp
```

Create a `.env` file with your bot token:

```
SLACK_BOT_TOKEN=xoxb-your-token-here
```

## Claude Code Configuration

Add to your `~/.claude.json` under `mcpServers`:

```json
"mcp-slack": {
  "command": "/path/to/mcp-slack/.venv/bin/python",
  "args": ["/path/to/mcp-slack/server.py"]
}
```

Replace `/path/to/mcp-slack` with the actual path where you cloned the repo.

If you use 1Password, you can inject the token via `op run` instead of a `.env` file:

```json
"mcp-slack": {
  "command": "/opt/homebrew/bin/op",
  "args": ["run", "--", "/path/to/mcp-slack/.venv/bin/python", "/path/to/mcp-slack/server.py"],
  "env": {
    "SLACK_BOT_TOKEN": "op://YourVault/YourItem/password"
  }
}
```

Restart Claude Code after updating the config.

## Security

- The `.env` file is gitignored and never committed
- If using Claude Code, add a deny rule for `.env` files so the agent cannot read your token
- Never paste your bot token into a conversation
