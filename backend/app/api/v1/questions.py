from fastapi import APIRouter, Depends

from app.core.dependencies import get_question_service
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.services.question import QuestionService

router = APIRouter()


@router.post("/flows/{flow_id}/questions", response_model=QuestionResponse, status_code=201)
async def create_question(
    flow_id: int,
    body: QuestionCreate,
    question_service: QuestionService = Depends(get_question_service),
) -> QuestionResponse:
    return await question_service.create(
        question_text=body.question_text,
        flow_id=flow_id,
        is_last=body.question_is_last,
        parent_id=body.question_parent_id,
        button_json=body.question_button_json,
    )


@router.get("/flows/{flow_id}/questions", response_model=list[QuestionResponse])
async def list_questions(
    flow_id: int,
    question_service: QuestionService = Depends(get_question_service),
) -> list[QuestionResponse]:
    return await question_service.list_by_flow(flow_id)


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    question_service: QuestionService = Depends(get_question_service),
) -> QuestionResponse:
    return await question_service.get_by_id(question_id)


@router.patch("/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    body: QuestionUpdate,
    question_service: QuestionService = Depends(get_question_service),
) -> QuestionResponse:
    return await question_service.update(
        question_id,
        question_text=body.question_text,
        question_is_last=body.question_is_last,
        question_is_delete=body.question_is_delete,
        question_button_json=body.question_button_json,
    )


@router.delete("/questions/{question_id}", status_code=204)
async def delete_question(
    question_id: int,
    question_service: QuestionService = Depends(get_question_service),
) -> None:
    await question_service.delete(question_id)
