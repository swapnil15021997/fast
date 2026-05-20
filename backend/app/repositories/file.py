from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File


class FileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, flow_id: str, file_path: str, file_name: str, file_size: int = 0, file_type: str = ""
    ) -> File:
        f = File(
            file_id=str(uuid4()),
            flow_file_id=flow_id,
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
        )
        self._session.add(f)
        await self._session.flush()
        return f

    async def get_by_id(self, file_id: str) -> File | None:
        return await self._session.get(File, file_id)

    async def list_by_flow(self, flow_id: str) -> list[File]:
        result = await self._session.execute(
            select(File).where(File.flow_file_id == flow_id).order_by(File.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete(self, file: File) -> None:
        await self._session.delete(file)
        await self._session.flush()
