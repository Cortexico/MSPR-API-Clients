from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.post("/customers", response_model=schemas.Customer)
async def create_customer(
    customer: schemas.CustomerCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_customer(db=db, customer=customer)


@router.get("/customers/{customer_id}", response_model=schemas.Customer)
async def read_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_customer = await crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return db_customer


@router.get("/customers", response_model=list[schemas.Customer])
async def read_customers(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    customers = await crud.get_customers(db, skip=skip, limit=limit)
    return customers


@router.put("/customers/{customer_id}", response_model=schemas.Customer)
async def update_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_customer = await crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return db_customer


@router.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_customer = await crud.delete_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return {"detail": "Client supprimé"}
