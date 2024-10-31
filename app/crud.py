from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):



    db_customer = get_customer(db, customer_id)
    if db_customer:
        for key, value in customer.dict(exclude_unset=True).items():
            setattr(db_customer, key, value)
        try:
            db.commit()
            db.refresh(db_customer)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email déjà enregistré")
        return db_customer
    else:
        raise HTTPException(status_code=404, detail="Client non trouvé")


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return db_customer
    else:
        raise HTTPException(status_code=404, detail="Client non trouvé")
