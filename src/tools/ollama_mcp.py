import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import ListToolsResult, Tool, CallToolResult

class OllamaServer(Server):
    async def handle_list_tools(self, params) -> ListToolsResult:
        return ListToolsResult(
            tools=[Tool(name="chat", description="Echo simple")]
        )

    async def handle_call_tool(self, name: str, arguments: dict) -> CallToolResult:
        if name == "chat":
            msg = arguments.get("message", "")
            return CallToolResult(
                content=[{"type": "text", "text": f"Echo: {msg}"}]
            )
        return CallToolResult(
            content=[{"type": "text", "text": "Herramienta desconocida"}]
        )

async def main():
    server = OllamaServer("ollama-mcp")

    # ✅ NO se pasa el server al `async with`
    async with stdio_server() as (read, write):
        # ✅ Aquí se arranca el server con los streams correctos
        await server.run(read, write, initialization_options={})

if __name__ == "__main__":
    asyncio.run(main())
