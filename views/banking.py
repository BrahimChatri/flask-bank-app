from flask import (request, Blueprint, redirect, render_template, url_for, 
                  session)
from utils.storage import Storage
import utils.logger as logger
import uuid
from functools import wraps

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
    
    
@banking.route('/transfer', methods=['GET', 'POST'])
@login_required 
def transfer():
    return "transfer page"

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