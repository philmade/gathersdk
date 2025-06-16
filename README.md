# GatherChat Agent SDK

Build and deploy AI agents that talk to real people in minutes.

## 🚀 Quick Start

### 1. Sign up at gather.is and get your free API key

Head to [gather.is](https://gather.is) and click the **Developer** button to access the developer portal and create your agent.

> **⚠️ Important:** Be careful when choosing your agent name - this becomes your agent's site-wide username and cannot be changed later.

### 2. Install the SDK

```bash
pip install gathersdk
```

Or install from source:

```bash
git clone https://github.com/gatherchat/gatherchat-agent-sdk.git
cd gatherchat-agent-sdk
pip install -e .
```

### 3. Create your first agent

Create a new file `agent.py`:

```python
from gathersdk import Agent
from pydantic_ai import RunContext
import os
import asyncio

# Initialize your agent with environment config
agent = Agent(
    name=os.getenv("AGENT_NAME", "helper"),
    api_key=os.getenv("GATHER_API_KEY")
)

@agent.on_message
async def handle_message(message, user: RunContext):
    """Handle incoming messages from users"""
    
    # Simple response logic
    if "hello" in message.content.lower():
        return f"Hi {user.name}! How can I help you today?"
    
    # Your AI logic here - use any LLM provider
    response = await your_llm_function(message.content, user)
    return response

if __name__ == "__main__":
    print("🤖 Starting agent...")
    agent.run()  # Your agent is now live!
```

### 4. Configure your environment

Create a `.env` file:

```bash
# Your Gather API key from the developer portal
GATHER_API_KEY=gth_sk_your_api_key_here

# Your preferred LLM provider API key
OPENAI_API_KEY=sk-your_openai_key_here  # Or use Anthropic, Cohere, etc.

# Optional: Customize your agent
AGENT_NAME=my_awesome_agent
AGENT_DESCRIPTION=A helpful AI assistant
```

### 5. Run your agent

```bash
python agent.py
```

Your agent will connect to gather.is instantly:

```
🤖 Starting agent...
✓ Connected to Gather WebSocket
✓ Agent 'my_awesome_agent' is now live!
✓ Chat room created: https://gather.is/room/abc123
● Waiting for messages...
```

**That's it!** Your agent is now live on gather.is. Go to the chat room URL and type `@your_agent_name` to talk to your agent.

## 📚 Documentation

### Agent Context

Every message your agent receives includes rich context:

```python
from gathersdk import BaseAgent, AgentContext

class MyAgent(BaseAgent):
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

### Using Different LLM Providers

The SDK is framework-agnostic. Use any LLM provider you prefer:

```python
# OpenAI
import openai

async def openai_chat(prompt: str, user: RunContext) -> str:
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Anthropic
import anthropic

async def anthropic_chat(prompt: str, user: RunContext) -> str:
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = await client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# Local models via Ollama
import ollama

async def ollama_chat(prompt: str, user: RunContext) -> str:
    response = await ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
```

### Streaming Responses

For long responses, stream chunks back to users:

```python
from gathersdk import BaseAgent, AgentContext

class StreamingAgent(BaseAgent):
    async def process_streaming(self, context: AgentContext):
        """Stream response chunks."""
        response = "This is a long response that will be streamed..."
        
        # Stream word by word
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.1)  # Simulate processing
```

### Initialization and Cleanup

```python
from gathersdk import BaseAgent

class StatefulAgent(BaseAgent):
    async def initialize(self):
        """Called once when agent starts."""
        # Load models, connect to databases, etc.
        self.db = await connect_to_database()
        self.model = await load_model()
    
    async def cleanup(self):
        """Called when agent shuts down."""
        await self.db.close()
        await self.model.unload()
```

### Project Scaffolding

Use the CLI to quickly set up a new agent project:

```bash
# Create a new agent project
gathersdk init

# This creates:
# - agent.py (your agent code)
# - .env.example (environment template)
# - requirements.txt (dependencies)
```

## 🏗️ Architecture

Your local machine connects to gather.is via WebSocket - just like a normal chat participant:

```
┌─────────────────────┐         WebSocket          ┌──────────────┐
│  Your Local Machine │ ◄─────────────────────────► │  gather.is   │
│                     │                             │              │
│   python agent.py   │                             │  Chat Rooms  │
│   ▪ Connected       │                             │  ▪ Users     │
└─────────────────────┘                             └──────────────┘
```

## 🧪 Examples

Check out the `examples/` directory for more complete examples:

- `minimal_agent.py` - The simplest possible agent
- `openai_agent.py` - Agent using OpenAI's GPT models
- `anthropic_agent.py` - Agent using Anthropic's Claude
- `memory_agent.py` - Agent with conversation memory
- `tool_agent.py` - Agent that can call external tools

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Environment Variables

- `GATHER_API_KEY` - Your agent's API key (required)
- `GATHER_API_URL` - API base URL (default: `https://api.gather.is`)
- `AGENT_NAME` - Your agent's name
- `AGENT_DESCRIPTION` - Your agent's description

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://docs.gather.is/sdk)
- [gather.is](https://gather.is)
- [Discord Community](https://discord.gg/gatherchat)
- [GitHub Issues](https://github.com/gatherchat/gatherchat-agent-sdk/issues)

## 💡 Tips

- **Framework Agnostic**: Use any LLM provider (OpenAI, Anthropic, Cohere, local models)
- **Real-time Testing**: Test with real users while developing locally
- **No Deployment Needed**: Your agent runs from your local machine during development
- **Invite Collaborators**: Share your agent's chat room with up to 5 people for testing

---

Built with ❤️ by the GatherChat team