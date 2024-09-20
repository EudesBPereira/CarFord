import pytest
from app.models import Car, Customer
from app import create_app
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

@pytest.fixture
def add_customer():
    # Adiciona um cliente no banco de dados de teste
    session = SessionLocal()
    new_customer = Customer(name="John Doe", email="john.doe@email.com", phone="123456789")
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    session.close()
    return new_customer.id

def test_get_cars(client):
    response = client.get('/api/cars')
    assert response.status_code == 200

def test_create_car(client, add_customer):
    new_car = {
        "owner_id": add_customer,
        "color": "Red",
        "model": "Sedan"
    }
    response = client.post('/api/car', json=new_car)
    assert response.status_code == 201
    data = response.get_json()
    assert data['color'] == "Red"
    assert data['model'] == "Sedan"

def test_create_car_exceeds_limit(client, add_customer):
    session = SessionLocal()
    
    # Adiciona 3 carros para um cliente
    for _ in range(3):
        new_car = Car(owner_id=add_customer, color="Blue", model="Hatchback")
        session.add(new_car)
    
    session.commit()
    session.close()

    # Tenta adicionar o quarto carro, que deve falhar
    new_car = {
        "owner_id": add_customer,
        "color": "Red",
        "model": "Sedan"
    }
    response = client.post('/api/car', json=new_car)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Um proprietário não pode ter mais de 3 carros cadastrados."

def test_update_car(client, add_customer):
    # Cria um carro para atualizar
    session = SessionLocal()
    car = Car(owner_id=add_customer, color="Blue", model="Hatchback")
    session.add(car)
    session.commit()
    session.refresh(car)
    car_id = car.id
    session.close()

    updated_car = {
        "owner_id": add_customer,
        "color": "Green",
        "model": "SUV"
    }
    response = client.put(f'/api/car/{car_id}', json=updated_car)
    assert response.status_code == 200
    data = response.get_json()
    assert data['color'] == "Green"
    assert data['model'] == "SUV"

def test_delete_car(client, add_customer):
    # Cria um carro para deletar
    session = SessionLocal()
    car = Car(owner_id=add_customer, color="Blue", model="Hatchback")
    session.add(car)
    session.commit()
    session.refresh(car)
    car_id = car.id
    session.close()

    # Deleta o carro
    response = client.delete(f'/api/car/{car_id}')
    assert response.status_code == 204
