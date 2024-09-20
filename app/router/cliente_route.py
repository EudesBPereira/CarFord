from flask import request, jsonify, abort
from . import cliente_routes 
from models import Customer
from .vehicle_routes import Car
from flask_jwt_extended import jwt_required
from shared.database import SessionLocal


@cliente_routes.route('/clientes', methods=['GET'])
@jwt_required()
def get_clientes():
    session = SessionLocal()
    clientes = session.query(Customer).all()
    session.close()
    
    result = []
    for cliente in clientes:
        cliente_data = {
            'id': cliente.id,
            'name': cliente.name,
            'email': cliente.email,
            'phone': cliente.phone,
            'address': cliente.address,
            'has_opportunity': cliente.has_opportunity
        }
        result.append(cliente_data)
    
    return jsonify(result)


@cliente_routes.route('/cliente/<int:id>', methods=['GET'])
@jwt_required()
def get_cliente(id):
    session = SessionLocal()
    cliente = session.query(Customer).filter_by(id=id).first()
    session.close()
    
    if cliente is None:
        abort(404, description="Cliente não encontrado")
    
    cliente_data = {
        'id': cliente.id,
        'name': cliente.name,
        'email': cliente.email,
        'phone': cliente.phone,
        'address': cliente.address,
        'has_opportunity': cliente.has_opportunity
    }
    
    return jsonify(cliente_data)

@cliente_routes.route('/cliente', methods=['POST'])
@jwt_required()
def create_cliente():
    data = request.json
    
    # Verifica se os campos obrigatórios estão presentes e não vazios
    if not data or not all(key in data and data[key].strip() for key in ['name', 'email', 'phone']):
        return jsonify({"error": "Verifique: 'name', 'email', e 'phone' são requeridos e não podem estar vazios."}), 400

    new_cliente = Customer(
        name=data['name'].strip(), 
        email=data['email'].strip(),
        phone=data['phone'].strip(), 
        address=data.get('address', '').strip(),
        has_opportunity=data.get('has_opportunity', True)
    )
    
    session = SessionLocal()
    session.add(new_cliente)
    session.commit()
    session.refresh(new_cliente)
    session.close()
    
    response_data = {
        'id': new_cliente.id,
        'name': new_cliente.name,
        'email': new_cliente.email,
        'phone': new_cliente.phone,
        'address': new_cliente.address,
        'has_opportunity': new_cliente.has_opportunity
    }
    
    return jsonify(response_data), 201



@cliente_routes.route('/cliente/<int:id>', methods=['PUT'])
@jwt_required()
def update_cliente(id):
    data = request.json
    session = SessionLocal()
    
    cliente = session.query(Customer).filter_by(id=id).first()
    
    if cliente is None:
        session.close()
        abort(404, description="Cliente não encontrado")
    
    # Verificar se está tentando atualizar has_opportunity para False
    if 'has_opportunity' in data and data['has_opportunity'] is False:
        # Verificar se o cliente tem carros registrados
        car_count = session.query(Car).filter_by(owner_id=id).count()
        
        if car_count == 0:
            session.close()
            abort(400, description="Não é possível definir has_opportunity como False, pois o cliente não possui carros.")
    
    cliente.name = data.get('name', cliente.name)
    cliente.email = data.get('email', cliente.email)
    cliente.phone = data.get('phone', cliente.phone)
    cliente.address = data.get('address', cliente.address)
    cliente.has_opportunity = data.get('has_opportunity', cliente.has_opportunity)
    
    session.commit()
    session.refresh(cliente)
    session.close()

    result = {
        'id': cliente.id,
        'name': cliente.name,
        'email': cliente.email,
        'phone': cliente.phone,
        'address': cliente.address,
        'has_opportunity': cliente.has_opportunity
    }
    
    return jsonify(result)


@cliente_routes.route('/cliente/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(id):
    session = SessionLocal()
    
    cliente = session.query(Customer).filter_by(id=id).first()
    if cliente is None:
        session.close()
        abort(404, description=f"Cliente com ID {id} não encontrado")

    session.delete(cliente)
    session.commit()
    session.close()
    
    return '', 204
