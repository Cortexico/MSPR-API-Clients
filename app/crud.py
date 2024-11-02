from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.rabbitmq_publisher import send_message_to_rabbitmq


# Obtenir un client par ID
async def get_customer(db: AsyncSession, customer_id: int):
    result = await db.execute(select(models.Customer).where(models.Customer.id == customer_id))
    return result.scalar_one_or_none()


# Obtenir tous les clients
async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Customer).offset(skip).limit(limit))
    return result.scalars().all()


# Créer un nouveau client
async def create_customer(db: AsyncSession, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    try:
        await db.commit()
        await db.refresh(db_customer)
        try:
            await send_message_to_rabbitmq({
                "action": "create",
                "data": {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
            })
        except Exception as e:
            print(f"Erreur d'envoi à RabbitMQ (création) : {e}")
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return db_customer


# Mettre à jour un client
async def update_customer(db: AsyncSession, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = await get_customer(db, customer_id)
    if db_customer:
        for key, value in customer.dict(exclude_unset=True).items():
            setattr(db_customer, key, value)
        try:
            await db.commit()
            await db.refresh(db_customer)
            try:
                await send_message_to_rabbitmq({
                    "action": "update",
                    "data": {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
                })
            except Exception as e:
                print(f"Erreur d'envoi à RabbitMQ (mise à jour) : {e}")
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Email déjà enregistré")
        return db_customer
    else:
        raise HTTPException(status_code=404, detail="Client non trouvé")


# Supprimer un client
async def delete_customer(db: AsyncSession, customer_id: int):
    db_customer = await get_customer(db, customer_id)
    if db_customer:
        await db.delete(db_customer)
        try:
            await db.commit()
            try:
                await send_message_to_rabbitmq({
                    "action": "delete",
                    "data": {"id": customer_id}
                })
            except Exception as e:
                print(f"Erreur d'envoi à RabbitMQ (suppression) : {e}")
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression")
        return db_customer
    else:
        raise HTTPException(status_code=404, detail="Client non trouvé")