import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import create_tables
from app.routers import customers
from app.rabbitmq_consumer import start_consumer

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

app.include_router(customers.router)

# Démarrer le consommateur RabbitMQ et créer les tables au démarrage de l'application
@app.on_event("startup")
def startup_event():
    create_tables()
    start_consumer()