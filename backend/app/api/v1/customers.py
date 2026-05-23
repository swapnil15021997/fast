from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_customer_service
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer import CustomerService

router = APIRouter()


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    body: CustomerCreate,
    user_id: str = Depends(get_current_user_id),
    customer_service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return await customer_service.create(
        user_id=user_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        address=body.address,
        company=body.company,
        notes=body.notes,
    )


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    customer_service: CustomerService = Depends(get_customer_service),
) -> list[CustomerResponse]:
    return await customer_service.list_all()


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    customer_service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return await customer_service.get_by_id(customer_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    body: CustomerUpdate,
    customer_service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return await customer_service.update(
        customer_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        address=body.address,
        company=body.company,
        notes=body.notes,
    )


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: str,
    customer_service: CustomerService = Depends(get_customer_service),
) -> None:
    await customer_service.delete(customer_id)
