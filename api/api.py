from flask import (request, Blueprint, session, jsonify)
from utils.storage import load_data, save_data
import utils.logger as logger
from utils.authmanager import *
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from datetime import timedelta
import os

load_dotenv()
KEY = os.getenv("ENCREPTION_KEY")
api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if username and password:
        if user_exists(username):
            encripted_data = load_data(username)
            user_data = decrypt_user_data(encripted_data, key=KEY)
            if compare_pass(password, user_data["password_hash"]):
                access_token = create_access_token(identity=username, expires_delta=timedelta(days=12))
                logger.Info_logger.info(f"User {username} logged in successfully via API")
                encripted_data["token"]= encrypt_data(access_token, key=KEY)
                save_data(encripted_data, username)
                return jsonify(access_token=access_token), 200

            else:
                return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "Username and password are required"}), 400

@api.route("/register", methods=["POST"])
def register():
    pass

@api.route('/balace', methods=['GET'])
@jwt_required()
def balance():
    token = request.headers.get("Authorization")