#!/usr/bin/env python3
"""
SQLite AI Agent - Clean persistent memory with SQLite
"""

import sys
import os
import sqlite3
import json
import logging
from typing import Optional

# Add the SDK to the path for this example
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO)

from gathersdk import MessageRouter
from gatherchat_agent_sdk.agent import AgentContext
from pydantic_ai import Agent as PydanticAgent, RunContext
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python

# Create your GatherChat message router
router = MessageRouter()

# Initialize Pydantic AI agent
ai_model = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o')
pydantic_agent = PydanticAgent(
    ai_model,
    deps_type=AgentContext,
    instructions="You are a helpful AI assistant with memory."
)

# SQLite setup
DB_PATH = "agent_memory.db"

def init_db():
    """Initialize SQLite database with chat_memories table"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_memories (
                chat_id TEXT PRIMARY KEY,
                messages TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def load_memory(chat_id: str) -> Optional[list]:
    """Load message history for chat from SQLite"""
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT messages FROM chat_memories WHERE chat_id = ?", 
            (chat_id,)
        ).fetchone()
        
        if row:
            return ModelMessagesTypeAdapter.validate_json(row[0])
    return None

def save_memory(chat_id: str, messages: list):
    """Save message history for chat to SQLite"""
    messages_json = json.dumps(to_jsonable_python(messages))
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO chat_memories (chat_id, messages, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (chat_id, messages_json))

@pydantic_agent.instructions
def add_context_instructions(ctx: RunContext[AgentContext]) -> str:
    """Generate dynamic instructions with memory context"""
    return f"You're chatting with {ctx.deps.user.display_name} in '{ctx.deps.chat.name}'."

@router.on_message
async def reply(ctx: AgentContext) -> str:
    """Handle messages with SQLite-backed memory"""
    try:
        # Load memory, run AI, save memory
        memory = load_memory(ctx.chat.chat_id)
        result = await pydantic_agent.run(ctx.prompt, deps=ctx, message_history=memory)
        save_memory(ctx.chat.chat_id, result.all_messages())
        
        return result.output
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Sorry, I encountered an error."

# Initialize database on import
init_db()

if __name__ == "__main__":
    print("🤖 Starting message router...")
    print(f"📍 Using model: {ai_model}")
    print(f"🗃️ Memory: {DB_PATH}")
    router.run()