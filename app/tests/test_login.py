import pytest
from flask import Flask
from app import create_app
from app.shared.database import SessionLocal, Base, engine

@pytest.fixture
def client():
    app = create_app()
    
    # Criar tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    
    with app.test_client() as client:
        yield client

    # Remover as tabelas depois dos testes
    Base.metadata.drop_all(bind=engine)

def test_login(client):
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    response = client.post('/api/login', json=login_data)
    
    # Verificar se o token foi retornado
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
