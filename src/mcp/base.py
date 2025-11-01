from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class MCPServer(ABC):
    """Base class for all MCP servers"""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an incoming request"""
        pass
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the MCP server"""
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup when shutting down"""
        pass