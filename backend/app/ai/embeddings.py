from app.ai.client import openai_client


async def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = await openai_client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding
