from fastapi import APIRouter

from app.api.v1 import auth, health, users, flows, questions, files, ai_models, tokens, chats, public, customers

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(flows.router, prefix="/flows", tags=["flows"])
api_router.include_router(questions.router, prefix="", tags=["questions"])
api_router.include_router(files.router, prefix="", tags=["files"])
api_router.include_router(ai_models.router, prefix="/ai-models", tags=["ai-models"])
api_router.include_router(tokens.router, prefix="/tokens", tags=["tokens"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(public.router, prefix="", tags=["public"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
