"""
GoGather Agent SDK

A Python SDK for building agents that integrate with GoGather WebSocket system.
"""

from .agent import (
    BaseAgent,
    AgentContext,
    UserContext,
    ChatContext,
    MessageContext,
    AgentResponse,
    AgentError,
)
from .client import AgentClient, run_agent
from .auth import SimpleAuth
from .router import MessageRouter
from .context_helpers import (
    serialize_agent_state,
    deserialize_agent_state,
    restore_or_create_agent_state,
    extract_agent_state_for_persistence,
    create_stateful_instructions,
    get_minimal_state,
    restore_from_minimal_state,
)

# Knowledge Graph functionality
from .knowledge_graph import (
    KnowledgeGraphManager,
    KGEntity,
    KGRelationship,
    KGSearchResult,
    create_kg_manager,
)
from .tools import (
    with_knowledge_graph,
    with_search_tracking,
    with_entity_creation,
    track_search,
    track_function,
    track_entity,
)
from .storage import create_storage_backend, DuckDBKGStorage
from .visualization import KGVisualizer, create_kg_visualizer, render_kg_snapshot

__version__ = "0.0.11"

__all__ = [
    # Core classes
    "BaseAgent",
    "AgentClient",
    "SimpleAuth",
    "MessageRouter",
    # Context models
    "AgentContext",
    "UserContext",
    "ChatContext",
    "MessageContext",
    # Helper classes
    "AgentResponse",
    "AgentError",
    # Convenience functions
    "run_agent",
    "format_conversation_history",
    # Agent state persistence helpers
    "serialize_agent_state",
    "deserialize_agent_state",
    "restore_or_create_agent_state",
    "extract_agent_state_for_persistence",
    "create_stateful_instructions",
    "get_minimal_state",
    "restore_from_minimal_state",
    # Knowledge Graph
    "KnowledgeGraphManager",
    "KGEntity",
    "KGRelationship",
    "KGSearchResult",
    "create_kg_manager",
    # Decorators
    "with_knowledge_graph",
    "with_search_tracking",
    "with_entity_creation",
    "track_search",
    "track_function",
    "track_entity",
    # Storage
    "create_storage_backend",
    "DuckDBKGStorage",
    # Visualization
    "KGVisualizer",
    "create_kg_visualizer",
    "render_kg_snapshot",
]
