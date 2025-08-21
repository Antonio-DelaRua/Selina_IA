import asyncio
import json
import websockets

async def send_request(tool, prompt, model=None):
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        payload = {
            "tool": tool,
            "prompt": prompt,
            "model": model
        }
        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        return json.loads(response)

async def main():
    # 🔹 1. Generar código
    result = await send_request("generate_code", "Crea una función Python que ordene una lista con QuickSort")
    print("\n🟢 generate_code:")
    print(result["response"])

    # 🔹 2. Resumir texto
    result = await send_request("summarize_text", "Python es un lenguaje de programación poderoso...")
    print("\n🟢 summarize_text:")
    print(result["response"])

    # 🔹 3. Usar modelo diferente (LLaMA3)
    result = await send_request("ollama_generate", "Dime un chiste sobre IA", model="llama3:latest")
    print("\n🟢 ollama_generate:")
    print(result["response"])

asyncio.run(main())
