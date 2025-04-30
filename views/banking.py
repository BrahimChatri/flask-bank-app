from flask import (request, Blueprint, redirect, render_template, url_for, 
                  session)
from utils.storage import Storage
import utils.logger as logger
import uuid, os
from utils.authmanager import AuthenticationManager
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv


banking = Blueprint('banking', __name__)

# Function to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


# home page for everyone
@banking.route('/')
def index():
    if session.get("user_id"):
        return redirect(url_for("banking.home"))
    return render_template("index.html")

# home page for loged in users that will show data 
@banking.route('/home')
@login_required
def home():
    user_data = Storage.load_data(session["username"])
    name = user_data.get("name")
    balance = user_data.get("balance")
    transactions = user_data.get("transactions", [])
    return render_template("home.html", balance=balance, transactions=transactions, username=session["username"], name=name)

@banking.route('/transactions', methods=['GET', 'POST'])
@login_required 
def transactions():
    user_data = Storage.load_data(session["username"])
    transactions = user_data.get("transactions", [])
    if not transactions :
        return render_template("transactions.html", transactions=transactions, message="No transactions found")
    

@banking.route("/transfer", methods=["POST"])
def transfer():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    recipient = request.form.get("recipient")
    message = request.form.get("message")
    try:
        amount = float(request.form.get("amount", 0))
    except ValueError:
        return render_template("home.html", error="Invalid amount entered.", show_modal=True, username=session["username"], balance=Storage.load_data(session["username"])["balance"])

    sender_username = session["username"]

    if not Storage.user_exists(recipient):
        return render_template("home.html", error="Recipient does not exist.", show_modal=True, username=sender_username, balance=Storage.load_data(sender_username)["balance"])

    sender_data = Storage.load_data(sender_username)
    recipient_data = Storage.load_data(recipient)

    if sender_data["balance"] < amount:
        return render_template("home.html", error="Insufficient funds.", show_modal=True, username=sender_username, balance=sender_data["balance"])

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
    Storage.save_data(sender_data, sender_username)
    Storage.save_data(recipient_data, recipient)

    logger.Info_logger.info(f"{sender_username} transferred {amount} to {recipient} at {now}")
    return render_template("home.html", success="Transfer completed successfully.", show_modal=True, username=sender_username, balance=sender_data["balance"])

@banking.route('/bills', methods=['GET', 'POST'])
@login_required 
def bills():
    return "bills page"

@banking.route('/settings', methods=['GET', 'POST'])
@login_required 
def settings():
    return "settings page"


@banking.route('/accounts', methods=['GET', 'POST'])
@login_required 
def accounts():
    return "accounts page"