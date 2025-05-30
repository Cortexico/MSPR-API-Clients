import pytest

@pytest.mark.asyncio
async def test_read_customers(client):
    # Ajouter un client de test à la base de données
    response = await client.post("/customers", json={
        "name": "John Doe",
        "email": "john@example.com",
        "address": "123 Main St"
    })
    assert response.status_code == 200

    # Récupérer la liste des clients
    response = await client.get("/customers")
    assert response.status_code == 200
    data = response.json()

    # Vérifier que le client ajouté est présent dans la réponse
    assert len(data) == 1
    assert data[0]["name"] == "John Doe"
    assert data[0]["email"] == "john@example.com"
    assert data[0]["address"] == "123 Main St"
