import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_clientes(client):
    response = client.get('/api/clientes')
    assert response.status_code == 200 

def test_create_cliente(client):
    new_cliente = {
        "name": "João Silva",
        "email": "joao.silva@email.com",
        "phone": "99999-9999",
        "address": "Rua A, 123"
    }

    response = client.post('/api/cliente', json=new_cliente)
    assert response.status_code == 201
