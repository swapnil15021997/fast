from fastapi import HTTPException, status

from app.repositories.file import FileRepository
from app.schemas.file import FileResponse


class FileService:
    def __init__(self, repo: FileRepository) -> None:
        self._repo = repo

    async def upload(
        self,
        flow_id: int,
        file_path: str,
        file_name: str,
        file_size: int = 0,
        file_type: str = "",
    ) -> FileResponse:
        f = await self._repo.create(flow_id, file_path, file_name, file_size, file_type)
        return FileResponse.model_validate(f)

    async def list_by_flow(self, flow_id: int) -> list[FileResponse]:
        files = await self._repo.list_by_flow(flow_id)
        return [FileResponse.model_validate(f) for f in files]

    async def delete(self, file_id: int) -> None:
        f = await self._repo.get_by_id(file_id)
        if not f:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
        await self._repo.delete(f)
