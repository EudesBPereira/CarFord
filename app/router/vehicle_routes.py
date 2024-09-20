from flask import request, jsonify, abort
from . import vehicle_routes
from flask_jwt_extended import jwt_required
from models import Car, Customer
from shared.database import SessionLocal

@vehicle_routes.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    session = SessionLocal()
    cars = session.query(Car).all()
    session.close()
    
    result = [{'id': c.id, 'owner_id': c.owner_id, 'color': c.color, 'model': c.model} for c in cars]
    return jsonify(result)

@vehicle_routes.route('/car/<int:id>', methods=['GET'])
@jwt_required()
def get_car(id):
    session = SessionLocal()
    car = session.query(Car).filter_by(id=id).first()
    session.close()
    
    if car is None:
        abort(404, description="Carro não encontrado")
    
    result = {'id': car.id, 'owner_id': car.owner_id, 'color': car.color, 'model': car.model}
    return jsonify(result)

@vehicle_routes.route('/car', methods=['POST'])
@jwt_required()
def create_car():
    data = request.json
    
    # Verificar se os campos estão presentes e não vazios
    if not data or any(key not in data or not data[key] for key in ['owner_id', 'color', 'model']):
        return jsonify({"error": "Os campos ('owner_id', 'color', e 'model') são requeridos e não podem ser vazios."}), 400

    session = SessionLocal()

    # Verificar se o cliente existe
    customer = session.query(Customer).filter_by(id=data['owner_id']).first()
    if not customer:
        session.close()
        return jsonify({"error": "Cliente não identificado, o owner_id fornecido não existe na tabela TB_CUSTOMER."}), 400

    # Verificar se o owner já possui 3 carros cadastrados
    car_count = session.query(Car).filter_by(owner_id=data['owner_id']).count()
    if car_count >= 3:
        session.close()
        return jsonify({"error": "Um proprietário não pode ter mais de 3 carros cadastrados."}), 400

    # Criar o novo carro
    new_car = Car(
        owner_id=data['owner_id'], 
        color=data['color'], 
        model=data['model']
    )
    
    session.add(new_car)
    session.commit()
    
    # Atualizar has_opportunity para False
    customer.has_opportunity = False
    session.commit()
    
    session.refresh(new_car)
    session.close()
    
    # Retornar todos os dados do carro cadastrado
    response_data = {
        'id': new_car.id,
        'owner_id': new_car.owner_id,
        'color': new_car.color,
        'model': new_car.model
    }
    
    return jsonify(response_data), 201



@vehicle_routes.route('/car/<int:id>', methods=['PUT'])
@jwt_required()
def update_car(id):
    data = request.json
    session = SessionLocal()
    
    car = session.query(Car).filter_by(id=id).first()
    if car is None:
        session.close()
        abort(404, description="Carro não encontrado")

    # Verificar se os campos estão presentes e não vazios
    if not data or any(key not in data or not data[key] for key in ['owner_id', 'color', 'model']):
        session.close()
        return jsonify({"error": "Os campos ('owner_id', 'color', e 'model') são requeridos e não podem ser vazios."}), 400

    new_owner_id = data['owner_id']

    # Verificar se o novo owner_id já possui 3 carros cadastrados
    if new_owner_id != car.owner_id:
        car_count = session.query(Car).filter_by(owner_id=new_owner_id).count()
        if car_count >= 3:
            session.close()
            return jsonify({"error": "Um proprietário não pode ter mais de 3 carros cadastrados."}), 400

    # Atualizar os dados do carro
    car.owner_id = new_owner_id
    car.color = data['color']
    car.model = data['model']
    
    session.commit()
    session.refresh(car)
    session.close()
    
    result = {
        'id': car.id,
        'owner_id': car.owner_id,
        'color': car.color,
        'model': car.model
    }
    
    return jsonify(result)



@vehicle_routes.route('/car/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_car(id):
    session = SessionLocal()
    car = session.query(Car).filter_by(id=id).first()
    
    if car is None:
        session.close()
        return jsonify({"error": "Carro não encontrado."}), 404
    
    owner_id = car.owner_id 
    session.delete(car)
    session.commit()

    # Verificar se o proprietario ainda possui carros
    temCarro = session.query(Car).filter_by(owner_id=owner_id).count()
    
    # Se não houver mais carros, atualizar has_opportunity
    if temCarro == 0:
        customer = session.query(Customer).filter_by(id=owner_id).first()
        if customer:
            customer.has_opportunity = True
            session.commit()
    
    session.close()
    return '', 204

