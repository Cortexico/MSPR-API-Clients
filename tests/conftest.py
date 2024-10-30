import sys
import os

# Définir les variables d'environnement avant d'importer les modules de l'application
os.environ["IS_TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Supprimer le fichier de base de données de test s'il existe déjà
if os.path.exists("./test.db"):
    os.remove("./test.db")

# Ajouter le répertoire racine du projet au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, engine
from app.main import app
from fastapi.testclient import TestClient

# Créer une session de base de données pour les tests
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Surcharger la dépendance get_db pour utiliser la session de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Créer les tables avant les tests et les supprimer après
@pytest.fixture(scope="module")
def client():
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Supprimer les tables
    Base.metadata.drop_all(bind=engine)
    # Supprimer le fichier de base de données de test
    if os.path.exists("./test.db"):
        os.remove("./test.db")
