from flask import request, jsonify
from werkzeug.security import generate_password_hash
from . import  register_routes
from models import User
from shared.database import SessionLocal

@register_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Os campos 'username' e 'password' são obrigatórios."}), 400

    # Criptografar a senha antes de armazenar
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Criar um novo usuário
    new_user = User(username=data['username'], password_hash=hashed_password)

    
    session = SessionLocal()
    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201
