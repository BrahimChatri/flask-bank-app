from flask import (request, Blueprint, redirect, render_template, url_for, session)
from utils.storage import Storage
import utils.logger as logger
from utils.authmanager import AuthenticationManager
import uuid, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("ENCREPTION_KEY")
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user_id"):
        return redirect(url_for("banking.home"))
        
    if request.method == "GET":
        return render_template("register.html")
    
    # POST method handling
    form = request.form
    username = form.get("username")
    
    if Storage.user_exists(username):
        logger.Error_logger.error(f"Registration failed: Username {username} already exists.")
        return render_template("register.html", error="Username already exists, please choose another")

    # Create new user
    password_hash = AuthenticationManager.hash_pass(password=form.get("password"))
    user_data = Storage.load_data(username)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

    name = form.get("name")
    email = form.get("email")
    phone_number = form.get("phone number")
    address = form.get("address")
    date_of_birth = form.get("date of birth")

    new_data = {
    "user_id": str(uuid.uuid4()),
    "username": username,
    "name": AuthenticationManager.encrypt_data(name, key=KEY),
    "email": AuthenticationManager.encrypt_data(email, key=KEY),
    "is_admin": False,
    "password_hash": password_hash,  
    "balance": 0,
    "account_number": str(uuid.uuid4().int)[:10],
    "phone_number": AuthenticationManager.encrypt_data(phone_number, key=KEY),
    "address": AuthenticationManager.encrypt_data(address, key=KEY),
    "date_created": formatted_date,
    "date_of_birth": AuthenticationManager.encrypt_data(date_of_birth, key=KEY),
    "transactions": user_data.get("transactions", []),
    "token": None,
}
    # old data structure for reference and debugging befor encryption
    # new_data = {
    #     "user_id": str(uuid.uuid4()),
    #     "username": username,
    #     "name": form.get("name"),
    #     "email": form.get("email"),
    #     "is_admin": False,
    #     "password_hash": password_hash,
    #     "balance": 0,
    #     "account_number": str(uuid.uuid4().int)[:10],
    #     "phone_number": form.get("phone number"),
    #     "address": form.get("address"),
    #     "date_created": formatted_date,
    #     "date_of_birth": form.get("date of birth"),
    #     "transactions": user_data.get("transactions", []),
    #     "token": None,
    # }
    
    Storage.save_data(new_data, username)
    logger.Info_logger.info(f"User {username} has registered successfully at {formatted_date}")
    return redirect(url_for("auth.login"))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for("banking.home"))
    
    if request.method == 'GET':
        return render_template("login.html")
    
    # POST method handling
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not Storage.user_exists(username):
        return render_template("login.html", error="Username does not exist")
        
    data = Storage.load_data(username)
    if not AuthenticationManager.compare_pass(password, data["password_hash"]):
        logger.Info_logger.warning(f"Failed login attempt for user: {username}")
        return render_template("login.html", error="Invalid password, try again")
    
    # Set session data
    session["user_id"] = data["user_id"]
    session["username"] = username
    session.permanent = bool(request.form.get("remember", False))
    
    logger.Info_logger.info(f"User {username} has logged in")
    return redirect(url_for("banking.home"))

@auth.route('/logout', methods=['POST'])
def logout():
    if session.get("user_id"):
        username = session.get("username")
        logger.Info_logger.info(f"User {username} has logged out")
        session.clear()
    return redirect(url_for("auth.login"))

@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")

    # POST: Verify identity
    username = request.form.get("username")
    email = request.form.get("email")

    if not Storage.user_exists(username):
        return render_template("forgot_password.html", error="Username not found.")

    user_data = Storage.load_data(username)
    if user_data.get("email") != email:
        return render_template("forgot_password.html", error="Email does not match our records.")

    # Store reset session and show reset form
    session["reset_username"] = username
    return render_template("forgot_password.html", success="Verified! You can now reset your password.", show_reset=True)

@auth.route("/reset_password", methods=["POST"])
def reset_password():
    username = session.get("reset_username")
    if not username or not Storage.user_exists(username):
        return redirect(url_for("auth.forgot_password"))

    new_password = request.form.get("new_password")
    if not new_password:
        return render_template("forgot_password.html", error="Password cannot be empty.", show_reset=True, success="Verified! You can now reset your password.")

    user_data = Storage.load_data(username)
    user_data["password_hash"] = AuthenticationManager.hash_pass(new_password)
    Storage.save_data(user_data, username)

    logger.Info_logger.info(f"Password reset for user: {username}")
    session.pop("reset_username", None)

    return redirect(url_for("auth.login"))