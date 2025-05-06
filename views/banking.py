from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.storage import load_data, save_data
import utils.logger as logger
import os, uuid
from utils.authmanager import *
from datetime import datetime
from dotenv import load_dotenv
from typing import Any

load_dotenv()
banking = Blueprint('banking', __name__)
KEY = os.getenv("ENCREPTION_KEY")


# home page for everyone
@banking.route('/', methods=['GET'])
def documentation():
    doc = {
        "message": "Welcome to the app! Please follow these steps to get started.",
        "steps": [
            {
                "step": 1,
                "description": "Go to /auth/login to log in to your account."
            },
            {
                "step": 2,
                "description": "After logging in, you will receive a token for authentication."
            },
            {
                "step": 3,
                "description": "Use the token for subsequent requests by including it in the Authorization header."
            },
            {
                "step": 4,
                "description": "For registration, go to /auth/register."
            },
            {
                "step": 5,
                "description": "For password reset, use /auth/forgot_password to receive a reset link."
            }
        ],
        "note": "Ensure to have all the required fields when registering or resetting your password."
    }
    return jsonify(doc), 200

# home page for loged in users that will show data 
@banking.route('/dashboard', methods=['GET'])
@jwt_required()
def home():
    encripted_data=load_data(get_jwt_identity())
    user_data = decrypt_user_data(encripted_data, key=KEY)
    api_data = user_data.copy()
    api_data.pop("password_hash", None)  # Remove sensitive data
    api_data.pop("user_id", None)
    api_data.pop("token", None)
    api_data.pop("phone_number", None)

    if not user_data:
        return jsonify({"error": "User data not found."}), 404
    return jsonify(api_data), 200

@banking.route('/transactions', methods=['GET', 'POST'])
@jwt_required() 
def transactions():
    enc_data: dict[str, Any] = load_data(get_jwt_identity())
    user_data: dict = decrypt_user_data(enc_data, key=KEY)
    transactions = user_data.get("transactions", [])
    if not transactions :
        return jsonify(transactions=transactions, message="No transactions found")
    return jsonify(
        transactions=transactions, 
        balance=user_data["balance"], 
        username=user_data["username"], 
        message="Transactions retrieved successfully", 
        first_name=user_data["first_name"]
        ), 200
    

@banking.route("/transfer", methods=["POST"])
@jwt_required()
def transfer():
    data = request.get_json()
    recipient = data.get("recipient")
    message = data.get("message")
    encrypted_data = load_data(get_jwt_identity())
    user_data =decrypt_user_data(encrypted_data, key=KEY)

    try:
        amount = float(data.get("amount", 0))
    except ValueError:
        return jsonify(
            error="Invalid amount entered.", 
            username=get_jwt_identity(), 
            balance=user_data["balance"]
            ), 400

    sender_username = user_data["username"]

    if not user_exists(recipient):
        return jsonify( 
            error="Recipient does not exist.", 
            username=sender_username, 
            balance=user_data["balance"]
            ), 404

    sender_data = load_data(sender_username)
    recipient_data = load_data(recipient)

    if sender_data["balance"] < amount:
        return jsonify( 
            error="Insufficient funds.",  
            username=sender_username, 
            balance=sender_data["balance"]
            ), 400

    # Perform transfer
    sender_data["balance"] -= amount
    recipient_data["balance"] += amount

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    transaction_id = str(uuid.uuid4())

    # Record transactions
    sender_data["transactions"].append({
        "id": transaction_id,
        "type": "debit",
        "amount": amount,
        "to": recipient,
        "message": "No message" if not message else message,
        "date": now
    })
    recipient_data["transactions"].append({
        "id": transaction_id,
        "type": "credit",
        "amount": amount,
        "from": sender_username,
        "message": "No message" if not message else message,
        "date": now
    })

    # Save changes
    save_data(sender_data, sender_username)
    save_data(recipient_data, recipient)

    logger.Info_logger.info(f"{sender_username} transferred {amount} to {recipient} at {now}")
    return jsonify( 
        success="Transfer completed successfully.", 
        username=sender_username, 
        balance=sender_data["balance"]
        ), 200


@banking.route('/pay_bills', methods=['GET', 'POST'])
@jwt_required() 
def bills():
    bills_category = ["Electricity", "Water", "Internet", "Gas", "Phone", "Insurance", "Rent", "Other"]

    # For GET requests, return available bill categories
    if request.method == 'GET':
        return jsonify({"bills_category": bills_category}), 200

    # For POST requests, process bill payment
    if request.method == 'POST':
        bill_type = request.form.get("bill_type")
        amount = request.form.get("amount")
        
        if bill_type not in bills_category:
            return jsonify({"error": "Invalid bill category."}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"error": "Invalid amount."}), 400

        user_data =  load_data(get_jwt_identity())

        if user_data["balance"] < amount:
            return jsonify({"error": "Insufficient funds."}), 400

        # Record the bill payment as a transaction
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = str(uuid.uuid4())

        user_data["balance"] -= amount
        user_data["transactions"].append({
            "id": transaction_id,
            "type": "debit",
            "amount": amount,
            "bill_type": bill_type,
            "date": now,
            "message": f"Paid {bill_type} bill"
        })

        # Save updated user data
        save_data(user_data, get_jwt_identity())
        
        return jsonify({"success": f"Successfully paid {bill_type} bill of {amount}.", "balance": user_data["balance"]}), 200

@banking.route('/profile', methods=['GET', 'POST'])
@jwt_required() 
def settings():
    user_data = load_data(get_jwt_identity())

    # For GET request, return current profile data
    if request.method == 'GET':
        return jsonify({
            "username": user_data["username"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": user_data["email"],
            "phone": user_data["phone"]
        }), 200

    # For POST request, update profile data
    if request.method == 'POST':
        new_first_name = request.form.get("first_name")
        new_last_name = request.form.get("last_name")
        new_email = request.form.get("email")
        new_phone = request.form.get("phone")

        # Validate new data
        if new_email:
            # You can add further validation for the email here
            user_data["email"] = decrypt_data(new_email, key=KEY)
        if new_phone:
            user_data["phone"] = decrypt_data(new_phone)
        if new_first_name:
            user_data["first_name"] = decrypt_data(new_first_name, key=KEY)
        if new_last_name:
            user_data["last_name"] = decrypt_data(new_last_name, key=KEY)

        # Save updated data
        save_data(user_data, get_jwt_identity())

        return jsonify({"success": "Profile updated successfully."}), 200


@banking.route('/balance', methods=['GET'])
@jwt_required()
def balance():
    data = load_data(get_jwt_identity())
    decrypted_data = decrypt_user_data(data, key=KEY)
    balance = decrypted_data.get("balance", 0)
    return jsonify({"balance": balance}), 200