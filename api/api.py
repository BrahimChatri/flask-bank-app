from flask import (request, Blueprint, session, jsonify)
from utils.storage import Storage
import utils.logger as logger
from utils.authmanager import AuthenticationManager
import uuid
from dotenv import load_dotenv
import os

KEY = os.getenv("ENCREPTION_KEY")
api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if AuthenticationManager.login_user(username, password):
        session['user'] = username
        user_data = Storage.load_data(username)
        token = str(uuid.uuid4())
        user_data['token'] = AuthenticationManager.encrypt_data(token, key=KEY)
        Storage.save_data(user_data, username)
        return jsonify(
            {"message": "Login successful",
            "token": token, 
            "documentation": "use ur token to request data in this api"}
            ), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
    
@api.route('/balace', methods=['GET'])
def balance():
    token = request.headers.get("Authorization")