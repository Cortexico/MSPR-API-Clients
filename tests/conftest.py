import sys
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, DATABASE_URL
from app.main import app
from httpx import AsyncClient

# Configurer la base de données de test en utilisant aiosqlite
os.environ["IS_TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

# Supprimer le fichier de base de données de test s'il existe déjà
if os.path.exists("./test.db"):
    os.remove("./test.db")

# Ajouter le répertoire racine du projet au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Utiliser un moteur asynchrone pour les tests
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

# Fonction asynchrone pour créer les tables
async def async_create_all():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Fonction asynchrone pour supprimer les tables
async def async_drop_all():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Surcharger la dépendance get_db pour utiliser la session de test
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Fixture pour préparer et nettoyer la base de données de test
@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    await async_create_all()
    yield
    await async_drop_all()

# Fixture pour le client asynchrone
@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
