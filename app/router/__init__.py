from flask import Blueprint

cliente_routes = Blueprint('cliente_routes', __name__)
vehicle_routes = Blueprint('vehicle_routes', __name__)
register_routes = Blueprint('register_routes', __name__)
login_routes = Blueprint('login_routes', __name__)

from router.cliente_route import cliente_routes
from router.vehicle_routes import vehicle_routes
from router.register_route import register_routes
from router.login_route import login_routes