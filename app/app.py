from flask import Flask
from flask_jwt_extended import JWTManager
from shared.database import engine, Base
from router import cliente_routes, vehicle_routes, register_routes, login_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    app.register_blueprint(cliente_routes, url_prefix='/api')
    app.register_blueprint(vehicle_routes, url_prefix='/api')
    app.register_blueprint(register_routes, url_prefix='/api')
    app.register_blueprint(login_routes, url_prefix='/api')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    app.run(debug=True)
