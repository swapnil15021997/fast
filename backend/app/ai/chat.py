from app.ai.client import openai_client
from app.core.config import settings


async def get_chat_response(prompt: str, model: str | None = None) -> str:
    response = await openai_client.chat.completions.create(
        model=model or settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""
