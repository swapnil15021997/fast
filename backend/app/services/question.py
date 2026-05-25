import json

from fastapi import HTTPException, status

from app.repositories.question import QuestionRepository
from app.schemas.question import QuestionResponse


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self._repo = repo

    async def create(
        self,
        question_text: str,
        flow_id: int,
        is_last: bool = False,
        parent_id: int | None = None,
        button_json: list[str] | None = None,
    ) -> QuestionResponse:
        q = await self._repo.create(
            question_text,
            flow_id,
            is_last,
            parent_id,
            json.dumps(button_json) if button_json is not None else None,
        )
        return QuestionResponse.model_validate(q)

    async def get_by_id(self, question_id: int) -> QuestionResponse:
        q = await self._repo.get_by_id(question_id)
        if not q or q.question_is_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        return QuestionResponse.model_validate(q)

    async def list_by_flow(self, flow_id: int) -> list[QuestionResponse]:
        questions = await self._repo.list_by_flow(flow_id)
        return [QuestionResponse.model_validate(q) for q in questions]

    async def update(self, question_id: int, **kwargs) -> QuestionResponse:
        q = await self._repo.get_by_id(question_id)
        if not q or q.question_is_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        cleaned = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            if key == "question_button_json":
                cleaned[key] = json.dumps(value)
            else:
                cleaned[key] = value
        if not cleaned:
            return QuestionResponse.model_validate(q)
        q = await self._repo.update(q, **cleaned)
        return QuestionResponse.model_validate(q)

    async def delete(self, question_id: int) -> None:
        q = await self._repo.get_by_id(question_id)
        if not q or q.question_is_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        await self._repo.soft_delete(q)
