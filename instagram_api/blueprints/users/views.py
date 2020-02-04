from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/<id>', methods=['GET'])
def a(id):
    user = User.get_by_id(id)
    return jsonify(id=user.id, username=user.username, email=user.email)
