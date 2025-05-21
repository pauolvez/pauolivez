# app/ollama_client.py

import httpx

OLLAMA_API_URL = "http://localhost:11434/api/generate"

async def generar_respuesta(prompt: str, model: str = "llama3"):
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_API_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json()["response"]