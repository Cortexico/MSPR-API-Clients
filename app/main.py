import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import engine, Base
from app.routers import customers
from app.rabbitmq_consumer import start_consumer

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

app.include_router(customers.router)

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Démarrer le consommateur RabbitMQ au démarrage de l'application
@app.on_event("startup")
async def startup_event():
    await start_consumer()
