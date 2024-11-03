from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import customers
from app.database import create_tables

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

# Inclure le routeur pour les clients
app.include_router(customers.router)


@app.on_event("startup")
async def startup_event():
    await create_tables()
