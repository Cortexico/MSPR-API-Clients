# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app import crud, schemas, models
# from app.database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

# router = APIRouter()

# # Dépendance pour obtenir la session de base de données
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/customers", response_model=schemas.Customer)
# def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
#     return crud.create_customer(db=db, customer=customer)

# @router.get("/customers/{customer_id}", response_model=schemas.Customer)
# def read_customer(customer_id: int, db: Session = Depends(get_db)):
#     db_customer = crud.get_customer(db, customer_id=customer_id)
#     if db_customer is None:
#         raise HTTPException(status_code=404, detail="Client non trouvé")
#     return db_customer

# @router.get("/customers", response_model=list[schemas.Customer])
# def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     customers = crud.get_customers(db, skip=skip, limit=limit)
#     return customers

# @router.put("/customers/{customer_id}", response_model=schemas.Customer)
# def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
#     db_customer = crud.update_customer(db, customer_id, customer)
#     if db_customer is None:
#         raise HTTPException(status_code=404, detail="Client non trouvé")
#     return db_customer

# @router.delete("/customers/{customer_id}")
# def delete_customer(customer_id: int, db: Session = Depends(get_db)):
#     db_customer = crud.delete_customer(db, customer_id)
#     if db_customer is None:
#         raise HTTPException(status_code=404, detail="Client non trouvé")
#     return {"detail": "Client supprimé"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/customers", response_model=schemas.Customer)
def create_customer(
    customer: schemas.CustomerCreate, db: Session = Depends(get_db)
):
    return crud.create_customer(db=db, customer=customer)

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return db_customer

@router.get("/customers", response_model=list[schemas.Customer])
def read_customers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    db_customer = crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return db_customer

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return {"detail": "Client supprimé"}
