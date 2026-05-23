from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: str, **kwargs) -> Customer:
        customer = Customer(customer_id=str(uuid4()), created_by=user_id, **kwargs)
        self._session.add(customer)
        await self._session.flush()
        return customer

    async def get_by_id(self, customer_id: str) -> Customer | None:
        return await self._session.get(Customer, customer_id)

    async def list_all(self) -> list[Customer]:
        result = await self._session.execute(
            select(Customer).order_by(Customer.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, customer: Customer, **kwargs) -> Customer:
        for key, value in kwargs.items():
            setattr(customer, key, value)
        await self._session.flush()
        return customer

    async def delete(self, customer: Customer) -> None:
        await self._session.delete(customer)
        await self._session.flush()
