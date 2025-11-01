from typing import Dict, Any
from .base import MCPServer
from sqlalchemy import func
from ..core.model import PythonDB, engine, sessionmaker

class DatabaseMCP(MCPServer):
    """MCP server for handling database operations"""
    
    def __init__(self):
        super().__init__("database_mcp")
        self.Session = sessionmaker(bind=engine)
        
    async def initialize(self) -> None:
        """Nothing to initialize for database"""
        pass
        
    async def shutdown(self) -> None:
        """Cleanup database connections"""
        pass
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle database queries"""
        action = request.get("action")
        if action == "query":
            return await self._handle_query(request.get("prompt", ""))
        elif action == "save":
            return await self._handle_save(request)
        return {"error": "Unknown action"}
        
    async def _handle_query(self, prompt: str) -> Dict[str, Any]:
        """Search for a prompt in the database"""
        session = self.Session()
        try:
            # Normalize prompt
            prompt = prompt.strip().lower()
            
            # Search with case-insensitive comparison
            result = session.query(PythonDB).filter(
                func.lower(PythonDB.prompt) == prompt
            ).first()
            
            if result:
                return {
                    "found": True,
                    "response": result.response,
                    "source": "database"
                }
            return {"found": False}
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            session.close()
            
    async def _handle_save(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Save a new prompt-response pair"""
        session = self.Session()
        try:
            prompt = request.get("prompt")
            response = request.get("response")
            if not prompt or not response:
                return {"error": "Missing prompt or response"}
                
            entry = PythonDB(prompt=prompt, response=response)
            session.add(entry)
            session.commit()
            return {"success": True}
            
        except Exception as e:
            session.rollback()
            return {"error": str(e)}
        finally:
            session.close()