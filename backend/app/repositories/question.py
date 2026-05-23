from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.question import Question


class QuestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        question_text: str,
        flow_id: str,
        is_last: bool = False,
        parent_id: str | None = None,
        button_json: str | None = None,
    ) -> Question:
        q = Question(
            question_id=str(uuid4()),
            question_text=question_text,
            question_is_last=is_last,
            question_parent_id=parent_id,
            question_flow_id=flow_id,
            question_button_json=button_json,
        )
        self._session.add(q)
        await self._session.flush()
        return q

    async def get_by_id(self, question_id: str) -> Question | None:
        return await self._session.get(Question, question_id)

    async def list_by_flow(self, flow_id: str) -> list[Question]:
        result = await self._session.execute(
            select(Question)
            .where(Question.question_flow_id == flow_id, Question.question_is_delete == False)
            .order_by(Question.created_at.asc())
        )
        return list(result.scalars().all())

    async def update(self, question: Question, **kwargs) -> Question:
        for key, value in kwargs.items():
            setattr(question, key, value)
        await self._session.flush()
        return question

    async def soft_delete(self, question: Question) -> None:
        question.question_is_delete = True
        await self._session.flush()
