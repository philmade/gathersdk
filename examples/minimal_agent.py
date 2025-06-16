#!/usr/bin/env python3
"""
Minimal GatherChat Agent Example

This is the simplest possible agent that echoes back what users say.
Perfect starting point for building your own agent!
"""

from gatherchat_agent_sdk import Agent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create your agent
agent = Agent()

@agent.on_message
async def handle_message(message: str, user: str) -> str:
    """
    Handle incoming messages from users.
    
    Args:
        message: The user's message text
        user: The user's display name
        
    Returns:
        The agent's response
    """
    return f"Hello {user}! You said: '{message}'"

if __name__ == "__main__":
    print("🤖 Starting minimal agent...")
    agent.run()