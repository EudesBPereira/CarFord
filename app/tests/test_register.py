import pytest
from app import create_app
from app.models import User
from app.shared.database import Base, engine, SessionLocal

@pytest.fixture
def app():
    app = create_app()

    # Criar as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)

    yield app

    # Dropar as tabelas ao final dos testes
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

def test_register_user_success(client, db_session):
    # Dados para registrar um novo usuário
    register_data = {
        "username": "testuser",
        "password": "securepassword123"
    }

    response = client.post('/api/register', json=register_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Usuário criado com sucesso!"

    # Verificar se o usuário foi criado no banco de dados
    user = db_session.query(User).filter_by(username="testuser").first()
    assert user is not None
    assert user.username == "testuser"

def test_register_missing_fields(client):
    # Dados sem o campo 'password'
    register_data = {
        "username": "incompleteuser"
    }

    response = client.post('/api/register', json=register_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Os campos 'username' e 'password' são obrigatórios."

def test_register_duplicate_user(client, db_session):
    # Criar um usuário para simular duplicidade
    user = User(username="existinguser", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    # Tentar cadastrar o mesmo usuário
    register_data = {
        "username": "existinguser",
        "password": "anotherpassword123"
    }

    response = client.post('/api/register', json=register_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "Usuário já existe" in data.get("error", "")

    # Limpar o banco de dados ao final
    db_session.delete(user)
    db_session.commit()
