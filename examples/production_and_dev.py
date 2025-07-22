#!/usr/bin/env python3
"""
Demo showing how to use the GoGather Agent SDK with both production and local development.

Production (default):
- WebSocket: wss://gather.is/ws
- Uses GATHERCHAT_AGENT_KEY from environment

Local Development:
- WebSocket: ws://127.0.0.1:8090/ws (override with GATHERCHAT_WS_URL)
- Uses GATHERCHAT_AGENT_KEY from environment
"""

import os
import asyncio
import logging
from gatherchat_agent_sdk import BaseAgent, AgentContext, run_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoAgent(BaseAgent):
    """Demo agent that works with both production and local development."""
    
    def __init__(self):
        super().__init__(
            name="demo-agent", 
            description="Demo agent for production and local development"
        )
    
    async def process(self, context: AgentContext) -> str:
        """Process incoming messages."""
        user = context.user.username
        prompt = context.prompt
        
        # Get connection info to show where we're connected
        ws_url = os.getenv('GATHERCHAT_WS_URL', 'wss://gather.is/ws (default)')
        
        logger.info(f"Processing message from {user}: {prompt}")
        
        if "info" in prompt.lower():
            return (
                f"Hello {user}! Demo agent info:\n"
                f"• WebSocket: {ws_url}\n"
                f"• Environment: {'Development' if 'localhost' in ws_url else 'Production'}\n"
                f"• Agent: {self.name}"
            )
        else:
            return f"Hello {user}! You said: {prompt}"

def main():
    """Main function to run the agent."""
    # Check environment configuration
    api_key = os.getenv('GATHERCHAT_AGENT_KEY')
    ws_url = os.getenv('GATHERCHAT_WS_URL')
    
    if not api_key:
        print("❌ Error: GATHERCHAT_AGENT_KEY environment variable required")
        print("Set it in your .env file or environment")
        return
    
    print("🤖 GoGather Agent SDK Demo")
    print("=" * 50)
    print(f"🔑 API Key: {api_key[:8]}...")
    
    if ws_url:
        print(f"🌐 WebSocket URL: {ws_url} (override)")
        print("📍 Environment: Local Development")
    else:
        print("🌐 WebSocket URL: wss://gather.is/ws (default)")
        print("📍 Environment: Production")
    
    print()
    print("Environment Variables:")
    print("• GATHERCHAT_AGENT_KEY=your_api_key_here (required)")
    print("• GATHERCHAT_WS_URL=ws://127.0.0.1:8090/ws (optional, for local dev)")
    print()
    print("For local development, add to your .env file:")
    print("GATHERCHAT_WS_URL=ws://127.0.0.1:8090/ws")
    print()
    print("Test commands:")
    print("• @your-agent-name info    - Show connection info")
    print("• @your-agent-name hello   - Basic greeting")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Create and run agent
    agent = DemoAgent()
    try:
        run_agent(agent)
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()