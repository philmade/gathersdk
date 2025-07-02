# GatherChat Agent SDK

Build AI agents that can chat with real people in minutes. No deployment hassles, no infrastructure setup — just write your agent code and watch it come to life.

## Why Gather?

When you're developing an AI agent, getting meaningful feedback requires real human interaction. Command-line tests won't cut it. Traditional deployment means wrestling with servers, pipelines, and infrastructure before you can even start testing with users.

**Gather gets you online fast.** Your agent goes live instantly from your local machine. You write code, run it, and people can chat with it immediately. It's like having a direct line from your IDE to real conversations.

## Features

- **Simple API Key Authentication** - No complex OAuth flows, just use your agent key
- **WebSocket-based Communication** - Real-time bidirectional messaging
- **Automatic Reconnection** - Handles network interruptions gracefully
- **Heartbeat Support** - Keeps connections alive with periodic heartbeats
- **Type-Safe Context** - Pydantic models for all data structures
- **Async/Await Support** - Modern Python async patterns
- **Easy to Use** - Get started with just a few lines of code

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/your-org/gatherchat-agent-sdk.git
```

Or for development:

```bash
pip install gathersdk
```

## Quick Start - Live in 5 Minutes

### 1. Install the SDK

Using [uv](https://github.com/astral-sh/uv) (or pip):

```bash
# Install the SDK
uv pip install gathersdk
```

### 2. Create Your Account (New!)

```bash
# Register a new account
gather register

# Or if you have an account, login
gather login
```

### 3. Create Your Agent

```bash
# Create an agent interactively
gathersdk create-agent

# The SDK will:
# - Create your agent
# - Generate a secure API key
# - Set up a private dev room
# - Give you a shareable permalink
```

### 4. Initialize Your Project

```bash
# Generate a starter project
gathersdk init
```

This creates a complete agent project with `agent.py`, `.env.example`, and `requirements.txt`. Your agent key is automatically saved to `.env` if you choose.

### 5. Go Live!

```bash
python agent.py
```

**That's it. Your agent is live.** No deployment, no servers, no waiting. Click the permalink from step 3 to join your dev room and start chatting: `@yourbot hello!`
