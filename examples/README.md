# GatherChat Agent Examples

This directory contains working examples of GatherChat agents.

The GatherChat Agent SDK has been developed with **Pydantic AI** in mind, providing seamless integration with modern AI frameworks. However, the SDK is **completely framework-agnostic** - you can use it with any AI library, HTTP client, or custom logic. These examples demonstrate various approaches from simple string responses to sophisticated AI-powered agents.

## Getting Started

1. **Set up your agent key**:
   - Create an agent in the GatherChat Developer Portal
   - Copy your agent key
   - Update the `GATHERCHAT_AGENT_KEY` in `.env`

2. **Run the minimal example**:
   ```bash
   cd examples
   python minimal_agent.py
   ```

3. **Test your agent**:
   - Go to your agent's dev room in GatherChat
   - Send a message like "Hello!"
   - Your agent will respond: "Hello YourName! You said: 'Hello!'"

## Examples

### `minimal_agent.py`
The simplest possible agent. Perfect starting point for new developers.

**What it does**: Echoes back messages with a friendly greeting.

**Code pattern**:
```python
from gathersdk import MessageRouter

router = MessageRouter()

@router.on_message
async def reply(message: str, user: str) -> str:
    return f"Hello {user}! You said: '{message}'"

router.run()
```

### `pydantic_ai_agent.py`
An AI-powered agent using Pydantic AI for intelligent responses.

**What it does**: Uses a large language model to generate contextual responses.

**Setup**:
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API key (e.g., `export OPENAI_API_KEY=your-key`)
3. Optionally set model: `export PYDANTIC_AI_MODEL=openai:gpt-4o`

**Features**:
- Intelligent conversation with context awareness
- Includes recent chat history in prompts
- Supports multiple AI models (OpenAI, Anthropic, Google, etc.)
- Graceful error handling

**Code pattern**:
```python
from gathersdk import MessageRouter
from pydantic_ai import Agent as PydanticAgent, RunContext

router = MessageRouter()
ai = PydanticAgent('openai:gpt-4o', deps_type=AgentContext, 
                   instructions="Be helpful and concise")

@ai.instructions
def add_context(ctx: RunContext[AgentContext]) -> str:
    return f"You're chatting with {ctx.deps.user.username} in {ctx.deps.chat.name}"

@router.on_message
async def reply(ctx: AgentContext) -> str:
    result = await ai.run(ctx.prompt, deps=ctx)
    return result.output
```

### `stateful_ai_agent.py`
An advanced AI agent that maintains persistent memory across conversations.

**What it does**: Remembers previous conversations within each chat room, enabling natural multi-turn dialogue.

**Setup**:
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API key (e.g., `export OPENAI_API_KEY=your-key`)

**Features**:
- **Persistent Memory**: Remembers conversations across agent restarts
- **Per-Chat Memory**: Separate memory for each chat room
- **File-Based Storage**: Saves conversation history to JSON files
- **Memory Statistics**: Logs memory usage and status
- **Graceful Degradation**: Falls back gracefully if memory fails

**State Management**:
- Uses Pydantic AI's `message_history` parameter
- Serializes/deserializes message history to JSON
- Maintains in-memory cache + file persistence
- Automatic memory loading/saving

**Code pattern**:
```python
# Load previous conversation history
message_history = load_chat_memory(chat_id)

# Run AI with memory context
result = await ai.run(prompt, deps=ctx, message_history=message_history)

# Save updated conversation history
save_chat_memory(chat_id, result.all_messages())
```

### `sqlite_ai_agent.py`
A clean, production-ready AI agent with SQLite-backed persistent memory.

**What it does**: Maintains conversation memory using SQLite for reliable persistence.

**Setup**:
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API key (e.g., `export OPENAI_API_KEY=your-key`)
3. Run the agent - SQLite database is created automatically

**Features**:
- **SQLite Storage**: Reliable, concurrent-safe database storage
- **Minimal Code**: Clean, concise implementation (~60 lines)
- **Auto-Schema**: Database table created automatically on startup
- **Per-Chat Memory**: Isolated conversation history per chat room
- **Production Ready**: Built-in timestamping and atomic operations

**Why SQLite?**
- No external dependencies or setup required
- Handles concurrency and data integrity automatically  
- Built into Python - works everywhere
- Can be easily migrated to PostgreSQL/MySQL later
- Supports complex queries for analytics

**Code pattern**:
```python
# Simple 3-step pattern
memory = load_memory(chat_id)                    # Load from SQLite
result = await ai.run(prompt, message_history=memory)  # Process with AI
save_memory(chat_id, result.all_messages())     # Save to SQLite
```

## Framework Agnostic Examples

While these examples focus on **Pydantic AI** integration, the GatherChat SDK works with any framework:

- **OpenAI SDK**: `openai.ChatCompletion.create()`
- **Anthropic SDK**: `anthropic.Anthropic().messages.create()`
- **LangChain**: `ChatOpenAI().invoke()`
- **Ollama**: Local model integration
- **Custom APIs**: Any HTTP-based AI service
- **Rule-based**: No AI at all - just Python logic

The SDK provides rich `AgentContext` with chat history, user info, and participants - use it however you want!

## Next Steps

Once you have the minimal agent working:

1. **Modify the response logic** - Change what your agent says
2. **Add conditions** - Make your agent respond differently based on the message
3. **Access rich context** - Use the full `BaseAgent` class for more features
4. **Deploy to production** - Host your agent on a server

## Need Help?

- Check the main SDK README
- Look at the GatherChat documentation
- Join our Discord community