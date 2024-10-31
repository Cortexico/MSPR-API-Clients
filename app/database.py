import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "customers")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "apiCustomers")
POSTGRES_DB = os.getenv("POSTGRES_DB", "customers_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Fonction pour créer les tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dépendance pour obtenir la session de base de données

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

