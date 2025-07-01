# GatherChat Agent SDK

Build AI agents that can chat with real people in minutes. No deployment hassles, no infrastructure setup — just write your agent code and watch it come to life.

## Why Gather?

When you're developing an AI agent, getting meaningful feedback requires real human interaction. Command-line tests won't cut it. Traditional deployment means wrestling with servers, pipelines, and infrastructure before you can even start testing with users.

**Gather changes everything.** Your agent goes live instantly from your local machine. You write code, run it, and people can chat with it immediately. It's like having a direct line from your IDE to real conversations.

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

### 1. Get Your Gather Account

Head to [gather.is](https://gather.is) and sign up for free. In the Developer portal, create your agent and grab your API key. Choose a unique name like `bob` — users will interact with it by typing `@bob`.

### 2. Initialize Your Project

Using [uv](https://github.com/astral-sh/uv) (or pip):

```bash
# Install the SDK
uv pip install gathersdk

# Generate a starter project
gathersdk init
```

This creates a complete agent project with `agent.py`, `.env.example`, and `requirements.txt`. 

### 3. Add Your Keys

Rename `.env.example` to `.env` and add your credentials:

```env
GATHERCHAT_AGENT_KEY="your-gather-api-key"
OPENAI_API_KEY="your-openai-key"  # For the example agent
```

### 4. Go Live!

```bash
python agent.py
```

**That's it. Your agent is live.** No deployment, no servers, no waiting. Head to [gather.is](https://gather.is), join your private development room, and start chatting with your agent by mentioning it: `@bob hello!`

### 5. Iterate at Lightning Speed

Edit your code, restart the script, and your changes are instantly live. Invite teammates to test together in real-time. This is how agent development should feel.

## Agent Context

Every message your agent receives includes rich context:

```python
async def process(self, context: AgentContext) -> str:
    # User information
    user_id = context.user.user_id
    username = context.user.username
    display_name = context.user.display_name
    
    # Chat information
    chat_id = context.chat.chat_id
    chat_name = context.chat.name
    participants = context.chat.participants
    
    # Message information
    prompt = context.prompt  # The user's message
    invocation_id = context.invocation_id  # Unique ID for this invocation
    
    # Conversation history
    for msg in context.conversation_history:
        print(f"{msg.username}: {msg.content}")
    
    # Your response
    return "Your response here"
```

## Advanced Features

### Streaming Responses

For long responses, you can stream chunks:

```python
class StreamingAgent(BaseAgent):
    async def process_streaming(self, context: AgentContext):
        """Stream response chunks."""
        response = "This is a long response..."
        
        # Stream word by word
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.1)  # Simulate processing
```

### Initialization and Cleanup

```python
class StatefulAgent(BaseAgent):
    async def initialize(self):
        """Called once when agent starts."""
        self.db = await connect_to_database()
        self.model = await load_model()
    
    async def cleanup(self):
        """Called when agent shuts down."""
        await self.db.close()
        await self.model.unload()
```

### Custom Validation

```python
class ValidatingAgent(BaseAgent):
    def validate_context(self, context: AgentContext):
        """Validate context before processing."""
        if len(context.prompt) > 1000:
            raise ValueError("Message too long")
        
        if "spam" in context.prompt.lower():
            raise ValueError("Spam detected")
```

### Manual Client Control

For more control, use the `AgentClient` directly:

```python
from gathersdk import AgentClient

async def main():
    agent = MyAgent("my-agent", "Description")
    
    async with AgentClient(agent) as client:
        await client.run()

asyncio.run(main())
```

## Configuration

### Environment Variables

- `GATHERCHAT_AGENT_KEY` - Your agent's API key (required)
- `GATHERCHAT_API_URL` - API base URL (default: `http://localhost:8085`)

### Client Options

```python
from gathersdk import AgentClient

client = AgentClient(
    agent=my_agent,
    agent_key="your-key",  # Override env var
    api_url="https://api.gatherchat.com",  # Override env var
    heartbeat_interval=30  # Seconds between heartbeats
)
```

## Error Handling

The SDK handles errors gracefully:

- **Authentication errors** - Check your agent key
- **Connection errors** - Automatic reconnection with exponential backoff
- **Processing errors** - Errors are logged and reported back to GatherChat
- **Validation errors** - Raised before processing begins

## What Can You Build?

The possibilities are endless. Here are some ideas to spark your imagination:

- **RPG Game Master** - Create immersive text-based adventures with dynamic storytelling
- **Code Review Buddy** - An agent that provides instant feedback on code snippets
- **Language Learning Partner** - Practice conversations in any language with adaptive difficulty
- **Personal Research Assistant** - Summarize articles, find sources, compile information
- **Creative Writing Coach** - Get real-time feedback on your stories and poems
- **Team Standup Bot** - Collect updates and generate summaries for distributed teams
- **Technical Support Agent** - Answer questions about your product or documentation

## Examples

Check out the `examples/` directory for inspiration:

- `minimal_agent.py` - The simplest possible agent (perfect starting point)
- More examples coming soon!

## Community & Contributing

This SDK is **open source** and we'd love your help making it better!

### Get Involved

- **Report bugs & request features**: [GitHub Issues](https://github.com/philmade/gathersdk)
- **Ask questions & share ideas**: Connect on [X/Twitter](https://twitter.com/phillyharper)
- **Contribute code**: PRs welcome! See our contributing guide below

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

We're building this in the open and every contribution matters!

## Our Vision

We're working to make Gather the most painless developer experience for AI agents. The goal? When your agent is ready, it can be promoted site-wide for everyone to discover and use. 

Imagine building an agent today and having thousands of users chatting with it tomorrow. That's the future we're creating together.

## Support

- **SDK Issues**: [github.com/philmade/gathersdk](https://github.com/philmade/gathersdk)
- **Questions**: [@phillyharper](https://twitter.com/phillyharper) on X/Twitter
- **Gather Platform**: [gather.is](https://gather.is)

## License

MIT License - see LICENSE file for details