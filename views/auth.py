from flask import request, Blueprint, url_for, jsonify
from utils.storage import load_data, save_data
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask_mail import Message, Mail
from flask import current_app
from datetime import timedelta
import utils.logger as logger
from utils.authmanager import *
import uuid, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("ENCREPTION_KEY")
auth = Blueprint('auth', __name__)
BLACKLIST = set()
mail = Mail()

@auth.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    expires = request_data.get('rememberMe', False)
    expires_delta = timedelta(days=15) if expires  else timedelta(minutes=30)
    if not username :
        return jsonify({"error": "Username required"}), 400
    elif not password:
        return jsonify({"error": "Password required"}), 400
    if username and password:
        if user_exists(username):
            encripted_data = load_data(username)
            user_data = decrypt_user_data(encripted_data, key=KEY)
            if compare_pass(password, user_data["password_hash"]):
                access_token = create_access_token(identity=username, expires_delta=expires_delta)
                logger.Info_logger.info(f"User {username} logged in successfully via API")
                encripted_data["token"]= encrypt_data(access_token, key=KEY)
                logger.Info_logger.info(f"User {username} has logged in")
                save_data(encripted_data, username)
                return jsonify(token=access_token), 200

            else:
                return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "Username and password are required"}), 400

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200


@auth.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    username = form.get("username")
    password = form.get("password")
    
    if user_exists(username):
        logger.Error_logger.error(f"Registration failed: Username {username} already exists.")
        return jsonify({"error": "Username already exists"}), 400

    # Create new user
    if not username :
        logger.Error_logger.error(f"Registration failed: Username or password cannot be empty.")
        return jsonify({"error": "Username required"}), 400
    elif not password:
        logger.Error_logger.error(f"Registration failed: Username or password cannot be empty.")
        return jsonify({"error": "Password required"}), 400
    elif len(password) < 8:
        logger.Error_logger.error(f"Registration failed: Password is too short.")
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    password_hash = hash_pass(password=password)
    user_data = load_data(username)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

    # check if data is provided or just empty string to avoid error in encryption
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email")
    phone_number = form.get("phone_number")
    address = form.get("address")
    date_of_birth = form.get("date_of_birth")
    if not all([first_name, last_name, email, phone_number, address, date_of_birth]):
        logger.Error_logger.error(f"Registration failed: All fields are required.")
        return jsonify({"error": "All fields are required "}), 400

    # Encrypting sensitive data before saving
    new_data = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "first_name": encrypt_data(first_name, key=KEY),
        "last_name": encrypt_data(last_name, key=KEY),
        "email": encrypt_data(email, key=KEY),
        "is_admin": False,
        "password_hash": password_hash,  
        "balance": 0,
        "account_number": str(uuid.uuid4().int)[:10],
        "phone_number": encrypt_data(phone_number, key=KEY),
        "address": encrypt_data(address, key=KEY),
        "date_created": formatted_date,
        "date_of_birth": encrypt_data(date_of_birth, key=KEY),
        "transactions": user_data.get("transactions", []),
        "token": None,
    }
     # old data structure for reference and debugging befor encryption
    # new_data = {
    #     "user_id": str(uuid.uuid4()),
    #     "username": username,
    #     "first_name": form.get("first_name"),
    #     "last_name": form.get("last_name"),
    #     "email": form.get("email"),
    #     "is_admin": False,
    #     "password_hash": password_hash,
    #     "balance": 0,
    #     "account_number": str(uuid.uuid4().int)[:10],
    #     "phone_number": form.get("phone_number"),
    #     "address": form.get("address"),
    #     "date_created": formatted_date,
    #     "date_of_birth": form.get("date_of_birth"),
    #     "transactions": user_data.get("transactions", []),
    #     "token": None,
    # }
    print(new_data)
    save_data(new_data, username)
    logger.Info_logger.info(f"User {username} has registered successfully at {formatted_date}")
    return jsonify({"message": "User registered successfully", "redirict": url_for("auth.login")}), 201

@auth.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if not user_exists(username):
        return jsonify({"error": "User not found"}), 404

    user_data = load_data(username)
    decrypted_email = decrypt_data(user_data.get("email"), key=KEY)

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(username, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    user_data["reset_token"] = token
    save_data(user_data, username)

    reset_url = url_for("auth.reset_password_token", token=token, _external=True)

    msg = Message("Password Reset",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[decrypted_email])
    msg.body = f"Hi {username},\n\nTo reset your password, click the link below:\n{reset_url}\n\nThis link is valid for 10 minutes."
    
    try:
        mail.send(msg)
        logger.Info_logger.info(f"Password reset email sent to {username}")
        return jsonify({"message": "Password reset link sent to your email."}), 200
    except Exception as e:
        logger.Error_logger.error(f"Failed to send email to {username}: {e}")
        return jsonify({"error": "Failed to send email."}), 500
    
@auth.route("/reset_password/<token>", methods=["POST"])
def reset_password_token(token):
    data = request.get_json()
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"error": "New password is required"}), 400
    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        username = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=600)
    except SignatureExpired:
        return jsonify({"error": "Token has expired"}), 400
    except BadSignature:
        return jsonify({"error": "Invalid token"}), 400

    if not user_exists(username):
        return jsonify({"error": "User not found"}), 404

    user_data = load_data(username)
    if user_data.get("reset_token") != token:
        return jsonify({"error": "Invalid or reused token"}), 403

    user_data["password_hash"] = hash_pass(new_password)
    user_data.pop("reset_token", None)
    save_data(user_data, username)

    logger.Info_logger.info(f"User {username} has successfully reset their password.")
    return jsonify({"message": "Password reset successful"}), 200