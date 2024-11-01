from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import create_tables
from app.routers import customers
from app.rabbitmq_consumer import start_consumer, connect_to_rabbitmq

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

app.include_router(customers.router)

# Start consumer and create tables
@app.on_event("startup")
def startup_event():
    create_tables()
    print("Tentative de connexion à RabbitMQ...")
    connection = connect_to_rabbitmq()  # Tentative de connexion en boucle
    if connection:
        print("Connexion à RabbitMQ établie avec succès.")
        start_consumer()
    else:
        print("Impossible de se connecter à RabbitMQ après plusieurs tentatives.")
