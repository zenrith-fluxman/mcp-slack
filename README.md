# mcp-slack

MCP server for reading and posting Slack messages. Gives Claude Code (or any MCP client) the ability to list channels, read messages, and post to any channel in a Slack workspace.

## Tools

| Tool | Description |
|------|-------------|
| `slack_post` | Post a message to a channel |
| `slack_read` | Read recent messages from a channel |
| `slack_list_channels` | List all channels (optionally filter to joined only) |

## Bot Token

This server authenticates with Slack using a **Bot Token** (`xoxb-...`). A bot token is tied to a Slack App and gives it permission to read and post messages on behalf of the bot user.

To get a token, either:
- **Create your own Slack App** at [api.slack.com/apps](https://api.slack.com/apps), add the required scopes (see below), install it to your workspace, and copy the Bot User OAuth Token from the OAuth & Permissions page.
- **Get it from your workspace admin** if a Slack App already exists for your workspace.

### Required Bot Token Scopes

Add these under your Slack App's OAuth & Permissions page, then reinstall the app to your workspace:

| Scope | What it does |
|-------|-------------|
| `chat:write` | Post messages to channels |
| `channels:read` | List public channels |
| `channels:history` | Read messages in public channels |
| `groups:read` | List private channels |
| `groups:history` | Read messages in private channels |
| `im:read` | List DMs (optional) |
| `im:write` | Open DMs (optional) |
| `im:history` | Read DMs (optional) |

After installing the app, invite the bot to any channel you want it to access: `/invite @YourBot`

## Setup

```bash
git clone https://github.com/zenrith-fluxman/mcp-slack.git
cd mcp-slack
python -m venv .venv
source .venv/bin/activate
pip install slack_sdk mcp
```

Create a `.env` file with your token:

```
SLACK_TOKEN=xoxb-your-token-here
```

For multiple workspaces, add additional tokens with a suffix:

```
SLACK_TOKEN=xoxb-default-workspace-token
SLACK_TOKEN_WORK=xoxp-other-workspace-token
```

Then use `workspace="work"` in any tool call to target that workspace.

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
    "SLACK_TOKEN": "op://YourVault/YourItem/password"
  }
}
```

Restart Claude Code after updating the config.

## Security

- The `.env` file is gitignored and never committed
- If using Claude Code, add a deny rule for `.env` files so the agent cannot read your token
- Never paste your bot token into a conversation
