from typing import Dict, List, Type, Any
from .base import MCPServer
from .database_mcp import DatabaseMCP
from .llm_mcp import LLMMCP
from .voice_mcp import VoiceCommandMCP
from .system_control_mcp import SystemControlMCP

class MCPManager:
    """Manages all MCP servers"""
    
    def __init__(self):
        self.mcps: Dict[str, MCPServer] = {}
        
    async def initialize(self) -> None:
        """Initialize all MCPs"""
        # Register default MCPs
        await self.register_mcp(DatabaseMCP())
        await self.register_mcp(LLMMCP())
        await self.register_mcp(VoiceCommandMCP())
        await self.register_mcp(SystemControlMCP())
        
    async def register_mcp(self, mcp: MCPServer) -> None:
        """Register a new MCP server"""
        await mcp.initialize()
        self.mcps[mcp.name] = mcp
        
    async def handle_request(self, target_mcp: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate MCP"""
        if target_mcp not in self.mcps:
            return {"error": f"MCP '{target_mcp}' not found"}
            
        return await self.mcps[target_mcp].handle_request(request)
        
    async def shutdown(self) -> None:
        """Shutdown all MCPs"""
        for mcp in self.mcps.values():
            await mcp.shutdown()
            
    async def handle_python_query(self, prompt: str) -> Dict[str, Any]:
        """Special handler for Python queries that combines database and LLM"""
        # First try database
        db_response = await self.handle_request("database_mcp", {
            "action": "query",
            "prompt": prompt
        })
        
        if db_response.get("found"):
            return db_response
            
        # If not found, use LLM
        return await self.handle_request("llm_mcp", {
            "prompt": prompt
        })