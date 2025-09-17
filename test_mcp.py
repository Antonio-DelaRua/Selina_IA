import asyncio
import logging
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    # Prepara el lanzamiento del servidor MCP por stdio
    params = StdioServerParameters(command="python", args=["ollama_mcp.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("🔍 Listando herramientas disponibles...")
            tools = await session.list_tools()
            print("📦 Herramientas encontradas:", [t.name for t in tools])

            # Probar la herramienta "chat"
            print("🛠️ Llamando a la herramienta 'chat'...")
            try:
                result = await session.call_tool(
                    "chat",
                    {"message": "Hola MCP!"}
                )
                print("✅ Respuesta del MCP:", result)
            except Exception as e:
                print("❌ Error llamando a la herramienta:", e)

# Logs detallados
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())
