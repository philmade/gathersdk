"""
Context Helpers for Knowledge Graph Integration

Provides utilities to automatically set up knowledge graph support in AgentContext.
"""

import logging
import json
from datetime import datetime
from typing import Optional, TypeVar, Type, Any, Dict
from pydantic import BaseModel
from .agent import AgentContext
from .knowledge_graph import KnowledgeGraphManager, KGStorageBackend
from .storage import create_storage_backend

logger = logging.getLogger(__name__)


def ensure_kg_manager(context: AgentContext, storage_backend: Optional[KGStorageBackend] = None) -> KnowledgeGraphManager:
    """
    Ensure AgentContext has a KnowledgeGraphManager attached.
    
    Creates and caches a KG manager on the context if it doesn't exist.
    
    Args:
        context: The AgentContext to enhance
        storage_backend: Optional custom storage backend
        
    Returns:
        The KG manager attached to the context
    """
    if not hasattr(context, '_kg_manager'):
        if storage_backend:
            context._kg_manager = KnowledgeGraphManager(storage_backend)
        else:
            # Use in-memory storage by default
            context._kg_manager = KnowledgeGraphManager()
    
    return context._kg_manager


def init_persistent_kg(context: AgentContext, db_path: str = None) -> KnowledgeGraphManager:
    """
    Initialize persistent knowledge graph storage for an AgentContext.
    
    Args:
        context: The AgentContext to enhance
        db_path: Path to DuckDB file (defaults to in-memory if None)
        
    Returns:
        KG manager with DuckDB storage
    """
    storage = create_storage_backend("duckdb", db_path=db_path or ":memory:")
    context._kg_manager = KnowledgeGraphManager(storage)
    return context._kg_manager


async def render_kg_context(context: AgentContext, max_searches: int = 2, max_actions: int = 5) -> str:
    """
    Render knowledge graph as agent-readable context string.
    
    Args:
        context: AgentContext with KG data
        max_searches: Maximum recent searches to show
        max_actions: Maximum recent actions to show
        
    Returns:
        Formatted context string for agent instructions
    """
    kg_manager = ensure_kg_manager(context)
    return await kg_manager.render_context(max_searches, max_actions)


async def get_kg_stats(context: AgentContext) -> dict:
    """Get knowledge graph statistics for the given context"""
    kg_manager = ensure_kg_manager(context)
    return await kg_manager.get_stats()


# Convenience functions for common KG operations
async def add_search_to_kg(context: AgentContext, query: str, results: str, search_type: str = "web") -> str:
    """Add search results to context's knowledge graph"""
    kg_manager = ensure_kg_manager(context)
    return await kg_manager.add_search(query, results, search_type)


async def add_entity_to_kg(context: AgentContext, name: str, entity_type: str, properties: dict = None) -> str:
    """Add entity to context's knowledge graph"""
    kg_manager = ensure_kg_manager(context)
    return await kg_manager.add_entity(name, entity_type, properties)


async def add_function_call_to_kg(context: AgentContext, function_name: str, args: dict, result: str) -> str:
    """Add function call to context's knowledge graph"""
    kg_manager = ensure_kg_manager(context)
    return await kg_manager.add_function_call(function_name, args, result)


# KG Visualization Helpers
async def render_kg_snapshot(context: AgentContext, snapshot_context: str = "") -> str:
    """
    Render a visual snapshot of the knowledge graph state
    
    Args:
        context: AgentContext with KG data
        snapshot_context: Context string (e.g., "after search", "before response")
        
    Returns:
        Visual representation of current KG state
    """
    from .visualization import render_kg_snapshot
    kg_manager = ensure_kg_manager(context)
    return await render_kg_snapshot(kg_manager, snapshot_context)


async def print_kg_snapshot(context: AgentContext, snapshot_context: str = "") -> None:
    """
    Print a visual snapshot of the knowledge graph state to logs
    
    Args:
        context: AgentContext with KG data  
        snapshot_context: Context string for the snapshot
    """
    snapshot = await render_kg_snapshot(context, snapshot_context)
    logger.info(f"\n{snapshot}")


async def get_kg_compact_summary(context: AgentContext) -> str:
    """Get a compact one-line summary of KG state"""
    from .visualization import KGVisualizer
    kg_manager = ensure_kg_manager(context)
    visualizer = KGVisualizer(kg_manager)
    return await visualizer.render_compact_summary()


async def dump_kg_state(context: AgentContext) -> str:
    """Get complete structured dump of KG for debugging"""
    from .visualization import KGVisualizer
    kg_manager = ensure_kg_manager(context)
    visualizer = KGVisualizer(kg_manager)
    return await visualizer.render_structured_dump()


def format_conversation_history(agent_context: AgentContext, max_messages: int = 10) -> str:
    """
    Format conversation history for agents using custom dependencies.
    
    This is a convenience function for agents that don't use AgentContext directly
    but store it in custom dependency objects (like SearchBrowseGraph.agent_context).
    
    Args:
        agent_context: The AgentContext object containing conversation history
        max_messages: Maximum number of recent messages to include (default: 10)
        
    Returns:
        Formatted string with conversation history or empty string if no history
        
    Example:
        # For agents with custom dependencies like Deep Agent:
        if ctx.deps.agent_context:
            history = format_conversation_history(ctx.deps.agent_context, 5)
            return f"{history}Current user: {ctx.deps.agent_context.user.display_name}"
    """
    if not agent_context:
        return ""
        
    return agent_context.format_conversation_history(max_messages)


# === AGENT STATE PERSISTENCE HELPERS ===

# Type variable for dependency graph models
T = TypeVar('T', bound=BaseModel)

def serialize_agent_state(dependency_graph: BaseModel) -> str:
    """
    Serialize a dependency graph (Pydantic model) to JSON string for persistence.
    
    Args:
        dependency_graph: The agent's dependency graph (Pydantic model)
        
    Returns:
        JSON string representation of the dependency graph
        
    Example:
        # In agent factory or instructions function:
        duck_graph = DuckGraph(agent_context=context, session_id="duck_001")
        state_json = serialize_agent_state(duck_graph)
        
        # Store this in agent response for main.go to persist
        return {"agent_state": state_json, "response": result}
    """
    if not dependency_graph:
        return ""
    
    try:
        # Use model_dump_json for optimal serialization
        return dependency_graph.model_dump_json()
    except Exception as e:
        logger.warning(f"Failed to serialize agent state: {e}")
        return ""


def deserialize_agent_state(state_json: str, model_type: Type[T]) -> Optional[T]:
    """
    Deserialize JSON string back to a dependency graph (Pydantic model).
    
    Args:
        state_json: JSON string representation of the dependency graph
        model_type: The Pydantic model class to deserialize to
        
    Returns:
        Restored dependency graph instance or None if deserialization fails
        
    Example:
        # In agent factory, restore previous state:
        if context.agent_state:
            restored_graph = deserialize_agent_state(context.agent_state, DuckGraph)
            if restored_graph:
                # Use restored state
                duck_graph = restored_graph
            else:
                # Genesis case or invalid state - create new
                duck_graph = DuckGraph(agent_context=context, session_id="duck_001")
        else:
            # Genesis case - no prior state
            duck_graph = DuckGraph(agent_context=context, session_id="duck_001")
    """
    if not state_json:
        return None
    
    try:
        # Parse JSON and create model instance
        state_dict = json.loads(state_json)
        return model_type.model_validate(state_dict)
    except Exception as e:
        logger.warning(f"Failed to deserialize agent state: {e}")
        return None


def restore_or_create_agent_state(context: AgentContext, model_type: Type[T], **create_kwargs) -> T:
    """
    Helper to restore agent state from context or create new state (genesis case).
    
    This is the main helper function agents should use for state persistence.
    It handles both the restoration case and the genesis case automatically.
    
    Args:
        context: AgentContext with potential agent_state
        model_type: The dependency graph model class
        **create_kwargs: Additional keyword arguments for creating new state
        
    Returns:
        Either restored dependency graph or new instance
        
    Example:
        # Standard usage in agent factory:
        duck_graph = restore_or_create_agent_state(
            context, 
            DuckGraph, 
            agent_context=context,
            session_id=f"duck_{context.invocation_id}"
        )
        
        # The function automatically handles:
        # - If context.agent_state exists: restores from JSON
        # - If no agent_state (genesis): creates new instance with create_kwargs
    """
    # Try to restore from existing state first
    if context.agent_state:
        restored = deserialize_agent_state(context.agent_state, model_type)
        if restored:
            logger.info(f"Restored agent state: {type(restored).__name__}")
            # Update agent_context to current context (important!)
            if hasattr(restored, 'agent_context'):
                restored.agent_context = context
            return restored
        else:
            logger.info("Failed to restore agent state, creating new (genesis)")
    else:
        logger.info("No prior agent state found, creating new (genesis)")
    
    # Genesis case - create new state
    return model_type(**create_kwargs)


def get_minimal_state(dependency_graph: BaseModel, 
                      max_field_size: int = 1000,
                      excluded_fields: Optional[set] = None) -> Dict[str, Any]:
    """
    Generic function to get minimal state from any Pydantic model for persistence.
    
    This function intelligently reduces the size of the state by:
    - Truncating large strings
    - Limiting list sizes
    - Excluding specified fields
    - Handling nested models recursively
    
    Args:
        dependency_graph: Any Pydantic model (dependency graph)
        max_field_size: Maximum size for string fields (default: 1000 chars)
        excluded_fields: Set of field names to exclude from state
        
    Returns:
        Minimal state dictionary suitable for persistence
        
    Example:
        # For any agent's dependency graph:
        minimal_state = get_minimal_state(
            ctx.deps,
            max_field_size=500,
            excluded_fields={'agent_context', 'storage_manager'}
        )
    """
    if not dependency_graph:
        return {}
    
    excluded = excluded_fields or {'agent_context', 'storage_manager', '_kg_manager'}
    state = {}
    
    try:
        # Get the model dump
        full_state = dependency_graph.model_dump()
        
        for key, value in full_state.items():
            # Skip excluded fields
            if key in excluded:
                continue
            
            # Handle different types
            if value is None:
                state[key] = None
            elif isinstance(value, str):
                # Truncate long strings
                state[key] = value[:max_field_size] if len(value) > max_field_size else value
            elif isinstance(value, (int, float, bool)):
                # Keep primitives as-is
                state[key] = value
            elif isinstance(value, datetime):
                # Convert datetime to ISO string
                state[key] = value.isoformat()
            elif isinstance(value, list):
                # Limit list size and process items
                limited_list = value[:10]  # Keep only first 10 items
                state[key] = [
                    _process_list_item(item, max_field_size) 
                    for item in limited_list
                ]
            elif isinstance(value, dict):
                # Recursively process nested dicts (but limit depth)
                state[key] = _process_dict(value, max_field_size, depth=1, max_depth=2)
            else:
                # For other types, try to convert to string
                try:
                    str_value = str(value)
                    state[key] = str_value[:max_field_size] if len(str_value) > max_field_size else str_value
                except:
                    state[key] = "<complex_object>"
        
        return state
        
    except Exception as e:
        logger.warning(f"Failed to create minimal state: {e}")
        return {}


def _process_list_item(item: Any, max_size: int) -> Any:
    """Helper to process list items for minimal state"""
    if item is None:
        return None
    elif isinstance(item, (str, int, float, bool)):
        if isinstance(item, str) and len(item) > max_size:
            return item[:max_size]
        return item
    elif isinstance(item, datetime):
        return item.isoformat()
    elif isinstance(item, dict):
        # For dict items in lists, just keep key structure
        return {k: type(v).__name__ for k, v in item.items()}
    else:
        return type(item).__name__


def _process_dict(d: Dict, max_size: int, depth: int = 0, max_depth: int = 2) -> Dict:
    """Helper to process nested dicts with depth limit"""
    if depth >= max_depth:
        return {"<truncated>": f"{len(d)} items"}
    
    result = {}
    for key, value in list(d.items())[:20]:  # Limit to 20 keys
        if isinstance(value, dict):
            result[key] = _process_dict(value, max_size, depth + 1, max_depth)
        elif isinstance(value, str) and len(value) > max_size:
            result[key] = value[:max_size]
        elif isinstance(value, list):
            result[key] = f"<list[{len(value)}]>"
        else:
            result[key] = value
    
    return result


def restore_from_minimal_state(minimal_state: Dict[str, Any], 
                               model_type: Type[T],
                               context: AgentContext,
                               **override_kwargs) -> T:
    """
    Generic function to restore a dependency graph from minimal state.
    
    This function creates a new instance of the model with:
    - Values from the minimal state
    - Current agent context
    - Any override values
    
    Args:
        minimal_state: The minimal state dictionary
        model_type: The Pydantic model class to create
        context: Current AgentContext
        **override_kwargs: Values to override from state
        
    Returns:
        New instance of the model with restored state
        
    Example:
        graph = restore_from_minimal_state(
            state_dict,
            DuckGraph,
            context,
            agent_context=context  # Override with current context
        )
    """
    # Start with minimal state
    init_kwargs = minimal_state.copy()
    
    # Always use current context
    init_kwargs['agent_context'] = context
    
    # Apply any overrides
    init_kwargs.update(override_kwargs)
    
    # Remove any None values that might cause issues
    init_kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
    
    try:
        # Create the model instance
        return model_type(**init_kwargs)
    except Exception as e:
        logger.warning(f"Failed to restore from minimal state, using defaults: {e}")
        # Fallback: create with just context
        return model_type(agent_context=context, **override_kwargs)


def extract_agent_state_for_persistence(dependency_graph: BaseModel) -> Dict[str, Any]:
    """
    Extract agent state for persistence and return as response metadata.
    
    This helper is used by the hosted agent service to extract state from
    agents after execution for storage in the messages table.
    
    Args:
        dependency_graph: The agent's dependency graph after execution
        
    Returns:
        Dictionary with agent_state key for response metadata
        
    Example:
        # In hosted agent service or agent wrapper:
        result = await agent.run(prompt, deps=duck_graph)
        state_data = extract_agent_state_for_persistence(duck_graph)
        
        return {
            "success": True,
            "result": result.output,
            "agent_state": state_data.get("agent_state", "")
        }
    """
    state_json = serialize_agent_state(dependency_graph)
    return {"agent_state": state_json}


def create_stateful_instructions(base_instructions: str, dependency_graph: BaseModel) -> str:
    """
    Create dynamic instructions that include current agent state for context.
    
    This helper generates instructions that update based on the current state
    of the dependency graph, providing the agent with awareness of its state.
    
    Args:
        base_instructions: Base system prompt/instructions
        dependency_graph: Current dependency graph with state
        
    Returns:
        Enhanced instructions with current state context
        
    Example:
        # In agent instructions function:
        @agent.instructions  
        def dynamic_instructions(ctx: RunContext[DuckGraph]) -> str:
            base = "You are a DuckDB data analysis agent..."
            return create_stateful_instructions(base, ctx.deps)
    """
    if not dependency_graph:
        return base_instructions
    
    try:
        # Get current state summary
        state_dict = dependency_graph.model_dump()
        
        # Generate state context
        state_context = f"""
        
--- CURRENT AGENT STATE ---
{json.dumps(state_dict, indent=2, default=str)}
--- END STATE ---

"""
        
        # Add conversation history if available
        conversation_context = ""
        if hasattr(dependency_graph, 'agent_context') and dependency_graph.agent_context:
            history = dependency_graph.agent_context.format_conversation_history(5)
            if history:
                conversation_context = f"\n{history}"
        
        return f"{base_instructions}{state_context}{conversation_context}"
        
    except Exception as e:
        logger.warning(f"Failed to create stateful instructions: {e}")
        return base_instructions