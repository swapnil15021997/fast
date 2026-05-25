import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File as FileForm, HTTPException, status

from app.core.config import settings
from app.core.dependencies import get_current_user_id, get_file_service, get_flow_service
from app.schemas.file import FileResponse
from app.services.file import FileService
from app.services.flow import FlowService

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/flows/{flow_id}/files", response_model=FileResponse, status_code=201)
async def upload_file(
    flow_id: int,
    file: UploadFile = FileForm(...),
    user_id: int = Depends(get_current_user_id),
    file_service: FileService = Depends(get_file_service),
    flow_service: FlowService = Depends(get_flow_service),
) -> FileResponse:
    await flow_service.get_by_id(flow_id, user_id)
    os.makedirs(f"{UPLOAD_DIR}/{flow_id}", exist_ok=True)
    ext = os.path.splitext(file.filename or "file")[1]
    stored_name = f"{uuid.uuid4()}{ext}"
    file_path = f"{UPLOAD_DIR}/{flow_id}/{stored_name}"
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return await file_service.upload(
        flow_id=flow_id,
        file_path=file_path,
        file_name=file.filename or stored_name,
        file_size=len(content),
        file_type=file.content_type or "",
    )


@router.get("/flows/{flow_id}/files", response_model=list[FileResponse])
async def list_files(
    flow_id: int,
    user_id: int = Depends(get_current_user_id),
    file_service: FileService = Depends(get_file_service),
    flow_service: FlowService = Depends(get_flow_service),
) -> list[FileResponse]:
    await flow_service.get_by_id(flow_id, user_id)
    return await file_service.list_by_flow(flow_id)


@router.delete("/files/{file_id}", status_code=204)
async def delete_file(
    file_id: int,
    user_id: int = Depends(get_current_user_id),
    file_service: FileService = Depends(get_file_service),
) -> None:
    await file_service.delete(file_id)
