from typing import Dict, Any
from .base import MCPServer
from langchain_ollama import OllamaLLM

class LLMMCP(MCPServer):
    """MCP server for handling LLM operations"""
    
    def __init__(self):
        super().__init__("llm_mcp")
        self.llm = None
        
    async def initialize(self) -> None:
        """Initialize the LLM"""
        self.llm = OllamaLLM(
            model="codellama:latest",
            temperature=0.3,
            num_predict=900,
            repeat_penalty=1.2,
            num_gpu_layers=20,
        )
        
    async def shutdown(self) -> None:
        """Nothing specific to cleanup for LLM"""
        pass
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LLM queries"""
        if not self.llm:
            return {"error": "LLM not initialized"}
            
        try:
            prompt = request.get("prompt", "")
            response = self.llm.invoke(prompt)
            return {
                "response": response,
                "source": "llm"
            }
        except Exception as e:
            return {"error": str(e)}