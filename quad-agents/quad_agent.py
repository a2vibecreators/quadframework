"""
QUAD Agent Base Class
=====================

Foundation for all QUAD agents. Every agent inherits from this class.

Key Features:
- Self-healing: Auto-fix errors when APIs change
- Agent-to-agent: Communicate via SUMA WIRE
- PRETEXT: AI-modifiable code sections
- Sub-agent generation: Create specialized agents

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
Patent Pending (63/956,810) - QUAD Platform
"""

import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QUADAgent")


class AgentState(Enum):
    """Agent lifecycle states (QUAD LEAF concept)"""
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    HEALING = "healing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentConfig:
    """Configuration for QUAD Agent"""
    name: str
    version: str = "1.0.0"
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 30
    enable_self_heal: bool = True
    enable_logging: bool = True
    api_base_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    """Message format for agent-to-agent communication (SUMA WIRE)"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str = ""
    to_agent: str = ""
    action: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None


@dataclass
class AgentResult:
    """Standard result format from agent execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retries: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class QUADAgent(ABC):
    """
    Base class for all QUAD agents.

    Every agent in the QUAD system inherits from this class.
    Provides self-healing, agent communication, and sub-agent generation.

    Example:
        class MyAgent(QUADAgent):
            def execute_task(self, input_data: dict) -> dict:
                return {"result": "Hello from MyAgent"}

            def _get_pretext(self) -> str:
                return "# PRETEXT: Can modify greeting message"
    """

    # Class-level registry of all agents (SUMA WIRE routing)
    _agent_registry: Dict[str, 'QUADAgent'] = {}

    def __init__(self, config: Optional[AgentConfig] = None, name: str = None):
        """
        Initialize QUAD Agent.

        Args:
            config: Agent configuration
            name: Agent name (uses class name if not provided)
        """
        self.config = config or AgentConfig(name=name or self.__class__.__name__)
        self.name = self.config.name
        self.state = AgentState.IDLE
        self.children: List['QUADAgent'] = []
        self.parent: Optional['QUADAgent'] = None
        self._execution_history: List[AgentResult] = []

        # Register this agent for SUMA WIRE routing
        QUADAgent._agent_registry[self.name] = self

        if self.config.enable_logging:
            logger.info(f"Agent initialized: {self.name}")

    # ─────────────────────────────────────────────────────────────
    # CORE METHODS
    # ─────────────────────────────────────────────────────────────

    def run(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute agent with self-healing capability.

        This is the main entry point for running an agent.
        Handles retries, error recovery, and result tracking.

        Args:
            input_data: Input parameters for the task

        Returns:
            AgentResult with success status and data
        """
        start_time = time.time()
        retries = 0
        last_error = None

        self.state = AgentState.RUNNING

        while retries <= self.config.max_retries:
            try:
                # Execute the task
                result = self.execute_task(input_data)

                # Success
                self.state = AgentState.COMPLETED
                execution_time = time.time() - start_time

                agent_result = AgentResult(
                    success=True,
                    data=result,
                    execution_time=execution_time,
                    retries=retries
                )
                self._execution_history.append(agent_result)

                if self.config.enable_logging:
                    logger.info(f"Agent {self.name} completed in {execution_time:.2f}s")

                return agent_result

            except Exception as e:
                last_error = e
                retries += 1

                if self.config.enable_logging:
                    logger.warning(f"Agent {self.name} error (attempt {retries}): {e}")

                # Try self-healing if enabled
                if self.config.enable_self_heal and retries <= self.config.max_retries:
                    self.state = AgentState.HEALING
                    healed = self.self_heal(e, input_data)

                    if healed:
                        if self.config.enable_logging:
                            logger.info(f"Agent {self.name} self-healed, retrying...")
                        time.sleep(self.config.retry_delay)
                        continue

                # If not healed or out of retries, fail
                break

        # Failed after all retries
        self.state = AgentState.FAILED
        execution_time = time.time() - start_time

        agent_result = AgentResult(
            success=False,
            error=str(last_error),
            execution_time=execution_time,
            retries=retries
        )
        self._execution_history.append(agent_result)

        if self.config.enable_logging:
            logger.error(f"Agent {self.name} failed after {retries} retries: {last_error}")

        return agent_result

    def self_heal(self, error: Exception, input_data: Dict[str, Any]) -> bool:
        """
        Attempt to auto-fix errors.

        Override this method to implement custom self-healing logic.
        Default implementation handles common API errors.

        Args:
            error: The exception that occurred
            input_data: Original input data

        Returns:
            True if healing was successful, False otherwise
        """
        error_str = str(error).lower()

        # PRETEXT: Self-healing logic
        # Allowed: Modify retry parameters, update API endpoints
        # Restricted: Cannot change core business logic

        # Handle common error types
        if "timeout" in error_str:
            # Increase timeout for next retry
            self.config.timeout = int(self.config.timeout * 1.5)
            logger.info(f"Increased timeout to {self.config.timeout}s")
            return True

        elif "rate limit" in error_str or "429" in error_str:
            # Wait longer before retry
            self.config.retry_delay = self.config.retry_delay * 2
            logger.info(f"Rate limited, waiting {self.config.retry_delay}s")
            return True

        elif "connection" in error_str:
            # Connection error, worth retrying
            return True

        elif "not found" in error_str or "404" in error_str:
            # Resource not found, unlikely to heal
            return False

        # Unknown error, attempt retry anyway
        return True

    # ─────────────────────────────────────────────────────────────
    # AGENT COMMUNICATION (SUMA WIRE)
    # ─────────────────────────────────────────────────────────────

    def talk_to_agent(
        self,
        agent_name: str,
        action: str,
        payload: Dict[str, Any],
        wait_for_response: bool = True
    ) -> Optional[AgentResult]:
        """
        Communicate with another agent via SUMA WIRE.

        This enables agent-to-agent communication without tight coupling.
        Agents are discovered via the registry.

        Args:
            agent_name: Name of the target agent
            action: Action to perform
            payload: Data to send
            wait_for_response: Whether to wait for response

        Returns:
            AgentResult if waiting, None if async
        """
        # Create message
        message = AgentMessage(
            from_agent=self.name,
            to_agent=agent_name,
            action=action,
            payload=payload
        )

        if self.config.enable_logging:
            logger.info(f"SUMA WIRE: {self.name} -> {agent_name} ({action})")

        # Find target agent
        target_agent = QUADAgent._agent_registry.get(agent_name)

        if not target_agent:
            logger.error(f"Agent not found: {agent_name}")
            return AgentResult(
                success=False,
                error=f"Agent not found: {agent_name}"
            )

        # Route message to target
        if wait_for_response:
            return target_agent.receive_message(message)
        else:
            # Async - fire and forget (would use queue in production)
            target_agent.receive_message(message)
            return None

    def receive_message(self, message: AgentMessage) -> AgentResult:
        """
        Receive and process a message from another agent.

        Override this to handle incoming messages differently.

        Args:
            message: Incoming message from another agent

        Returns:
            AgentResult with response
        """
        if self.config.enable_logging:
            logger.info(f"SUMA WIRE: {self.name} received from {message.from_agent}")

        # Default: execute task with payload
        return self.run(message.payload)

    # ─────────────────────────────────────────────────────────────
    # SUB-AGENT GENERATION
    # ─────────────────────────────────────────────────────────────

    def generate_sub_agent(
        self,
        name: str,
        purpose: str,
        execute_fn: Callable[[Dict], Dict],
        pretext: str = ""
    ) -> 'QUADAgent':
        """
        Generate a specialized sub-agent dynamically.

        This is the core of "code that generates agents" concept.

        Args:
            name: Name for the new agent
            purpose: Description of what the agent does
            execute_fn: Function that implements execute_task
            pretext: AI-modifiable code description

        Returns:
            New QUADAgent instance
        """
        # Create dynamic agent class
        class DynamicAgent(QUADAgent):
            __doc__ = purpose
            _execute_fn = staticmethod(execute_fn)
            _pretext = pretext

            def execute_task(self, input_data: dict) -> dict:
                return self._execute_fn(input_data)

            def _get_pretext(self) -> str:
                return self._pretext

        # Instantiate and register as child
        config = AgentConfig(name=name)
        agent = DynamicAgent(config=config)
        agent.parent = self
        self.children.append(agent)

        if self.config.enable_logging:
            logger.info(f"Generated sub-agent: {name} (parent: {self.name})")

        return agent

    def generate_sub_agent_from_spec(self, spec: Dict[str, Any]) -> 'QUADAgent':
        """
        Generate sub-agent from a specification dictionary.

        Args:
            spec: Agent specification with keys:
                - name: Agent name
                - purpose: What the agent does
                - data_sources: List of data sources to query
                - capabilities: List of capabilities

        Returns:
            New QUADAgent instance
        """
        name = spec.get("name", f"Agent_{uuid.uuid4().hex[:8]}")
        purpose = spec.get("purpose", "Generated agent")
        data_sources = spec.get("data_sources", [])
        capabilities = spec.get("capabilities", [])

        # Generate execute function based on spec
        def execute_fn(input_data: dict) -> dict:
            return {
                "agent": name,
                "purpose": purpose,
                "data_sources": data_sources,
                "capabilities": capabilities,
                "input": input_data,
                "status": "executed"
            }

        pretext = f"""
# PRETEXT: {name}
# Purpose: {purpose}
# Data Sources: {', '.join(data_sources)}
# Capabilities: {', '.join(capabilities)}
# Allowed: Modify query parameters, add filters, change output format
# Restricted: Cannot delete data, cannot access unauthorized data sources
"""

        return self.generate_sub_agent(name, purpose, execute_fn, pretext)

    # ─────────────────────────────────────────────────────────────
    # ABSTRACT METHODS (Must Override)
    # ─────────────────────────────────────────────────────────────

    @abstractmethod
    def execute_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task.

        MUST be implemented by subclasses.

        Args:
            input_data: Input parameters

        Returns:
            Result dictionary
        """
        pass

    @abstractmethod
    def _get_pretext(self) -> str:
        """
        Return the PRETEXT for AI-modifiable code.

        MUST be implemented by subclasses.
        Documents what the AI can and cannot modify.

        Returns:
            PRETEXT string describing allowed modifications
        """
        pass

    # ─────────────────────────────────────────────────────────────
    # UTILITY METHODS
    # ─────────────────────────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "children": [c.name for c in self.children],
            "parent": self.parent.name if self.parent else None,
            "execution_count": len(self._execution_history),
            "last_result": self._execution_history[-1] if self._execution_history else None
        }

    def get_execution_history(self) -> List[AgentResult]:
        """Get execution history"""
        return self._execution_history.copy()

    @classmethod
    def get_registered_agents(cls) -> List[str]:
        """Get list of all registered agents"""
        return list(cls._agent_registry.keys())

    @classmethod
    def get_agent(cls, name: str) -> Optional['QUADAgent']:
        """Get agent by name from registry"""
        return cls._agent_registry.get(name)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize agent to dictionary"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "config": {
                "version": self.config.version,
                "max_retries": self.config.max_retries,
                "timeout": self.config.timeout
            },
            "state": self.state.value,
            "pretext": self._get_pretext(),
            "children": [c.to_dict() for c in self.children]
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, state={self.state.value})>"


# ─────────────────────────────────────────────────────────────────
# EXAMPLE USAGE
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Example: Create a simple agent

    class GreetingAgent(QUADAgent):
        """Simple agent that greets users"""

        def execute_task(self, input_data: dict) -> dict:
            name = input_data.get("name", "World")
            return {"greeting": f"Hello, {name}!"}

        def _get_pretext(self) -> str:
            return """
# PRETEXT: GreetingAgent
# Allowed: Modify greeting format, add time-based greetings
# Restricted: Cannot access external APIs
"""

    # Create and run
    agent = GreetingAgent()
    result = agent.run({"name": "QUAD"})
    print(f"Result: {result}")

    # Generate sub-agent
    sub_agent = agent.generate_sub_agent_from_spec({
        "name": "FormalGreeter",
        "purpose": "Formal greetings for business",
        "data_sources": ["user_preferences"],
        "capabilities": ["greet", "farewell"]
    })

    print(f"Sub-agent: {sub_agent}")
    print(f"Registered agents: {QUADAgent.get_registered_agents()}")
