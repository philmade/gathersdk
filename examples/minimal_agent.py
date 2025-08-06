#!/usr/bin/env python3
"""
Minimal Agent Example - The simplest possible GatherChat agent
"""

import sys
import os
# Add the SDK to the path for this example
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import logging
logging.basicConfig(level=logging.INFO)

from gathersdk import MessageRouter
from gatherchat_agent_sdk.agent import AgentContext

# Create your agent
router = MessageRouter()

@router.on_message
async def reply(ctx: AgentContext) -> str:
    """
    Handle incoming messages.
    
    Args:
        ctx: Rich context containing:
            - ctx.user: User who sent the message (username, display_name, etc.)
            - ctx.chat: Chat information (id, name, participants, etc.)
            - ctx.prompt: The message text content  
            - ctx.conversation_history: Recent messages for context
            - ctx.invocation_id: Unique ID for this invocation
        
    Returns:
        Your agent's response as a string
    """
    # Access rich context information
    user_name = ctx.user.display_name or ctx.user.username
    chat_name = ctx.chat.name
    message_text = ctx.prompt
    history_count = len(ctx.conversation_history)
    participant_count = len(ctx.chat.participants)
    
    return f"Hello {user_name}! You said: '{message_text}' in '{chat_name}'. I can see {history_count} recent messages and {participant_count} participants."

if __name__ == "__main__":
    print("🤖 Starting message router...")
    router.run()