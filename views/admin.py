from flask import request, Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.storage import load_data, save_data
from utils.authmanager import user_exists
from utils.authmanager import decrypt_user_data
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
admin = Blueprint('admin', __name__)
KEY = os.getenv("ENCREPTION_KEY")

# Helper function to check if the logged-in user is an admin
def is_admin():
    current_user = get_jwt_identity()
    user_data_encrypted = load_data(current_user + '.json')
    user_data = decrypt_user_data(user_data_encrypted, key=KEY)
    
    # Check if the user has 'is_admin' key and if it is True
    return user_data.get('is_admin', False)

# Admin homepage
@admin.route('/', methods=['GET'])
@jwt_required()
def admin_home():
    if not is_admin():
        return jsonify({"error": "Unauthorized access. Admins only."}), 403
    return render_template("admin_home.html")  # Create a template for admin's home page

# View all users
@admin.route('/users', methods=['GET'])
@jwt_required()
def view_users():
    if not is_admin():
        return jsonify({"error": "Unauthorized access. Admins only."}), 403

    users_data = []
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            user_data_encrypted = load_data(filename)
            user_data = decrypt_user_data(user_data_encrypted, key=KEY)
            users_data.append({
                "username": user_data["username"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "balance": user_data["balance"]
            })
    return jsonify(users_data), 200

# View a user's details
@admin.route('/user/<username>', methods=['GET'])
@jwt_required()
def view_user_details(username):
    if not is_admin():
        return jsonify({"error": "Unauthorized access. Admins only."}), 403

    if not user_exists(username):
        return jsonify({"error": "User not found."}), 404
    user_data_encrypted = load_data(username + '.json')
    user_data = decrypt_user_data(user_data_encrypted, key=KEY)
    return jsonify(user_data), 200

# Update a user's balance
@admin.route('/user/<username>/update_balance', methods=['POST'])
@jwt_required()
def update_balance(username):
    if not is_admin():
        return jsonify({"error": "Unauthorized access. Admins only."}), 403

    if not user_exists(username):
        return jsonify({"error": "User not found."}), 404

    new_balance = request.form.get("balance")
    try:
        new_balance = float(new_balance)
    except ValueError:
        return jsonify({"error": "Invalid balance value."}), 400

    user_data = load_data(username + '.json')
    user_data["balance"] = new_balance
    save_data(user_data, username + '.json')
    
    return jsonify({"message": "Balance updated successfully.", "new_balance": new_balance}), 200

# View all transactions
@admin.route('/transactions', methods=['GET'])
@jwt_required()
def view_transactions():
    if not is_admin():
        return jsonify({"error": "Unauthorized access. Admins only."}), 403

    transactions = []
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            user_data_encrypted = load_data(filename)
            user_data = decrypt_user_data(user_data_encrypted)
            transactions.extend(user_data.get("transactions", []))
    
    return jsonify(transactions), 200
