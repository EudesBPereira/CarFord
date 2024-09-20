from flask import request, jsonify
from . import login_routes
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User
from shared.database import SessionLocal
from datetime import timedelta

@login_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    session = SessionLocal()
    
    try:
        # Usar a sessão para consultar o usuário
        user = session.query(User).filter_by(username=username).first()

        # Verificar se o usuário existe e se a senha está correta
        if user and check_password_hash(user.password_hash, password):
            expires = timedelta(minutes=5) 
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return jsonify(access_token=access_token), 200

        return jsonify({"msg": "Usuário ou senha incorretos"}), 401
    finally:
        session.close()