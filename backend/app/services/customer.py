from fastapi import HTTPException, status

from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerResponse


class CustomerService:
    def __init__(self, repo: CustomerRepository) -> None:
        self._repo = repo

    async def create(self, user_id: str, **kwargs) -> CustomerResponse:
        customer = await self._repo.create(user_id, **kwargs)
        return CustomerResponse.model_validate(customer)

    async def get_by_id(self, customer_id: str) -> CustomerResponse:
        customer = await self._repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        return CustomerResponse.model_validate(customer)

    async def list_all(self) -> list[CustomerResponse]:
        customers = await self._repo.list_all()
        return [CustomerResponse.model_validate(c) for c in customers]

    async def update(self, customer_id: str, **kwargs) -> CustomerResponse:
        customer = await self._repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        cleaned = {k: v for k, v in kwargs.items() if v is not None}
        if not cleaned:
            return CustomerResponse.model_validate(customer)
        customer = await self._repo.update(customer, **cleaned)
        return CustomerResponse.model_validate(customer)

    async def delete(self, customer_id: str) -> None:
        customer = await self._repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        await self._repo.delete(customer)
