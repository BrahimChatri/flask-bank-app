from flask import (request, Blueprint, redirect, render_template, url_for, 
                  session)
from utils.storage import Storage
import utils.logger as logger
import uuid
from functools import wraps

banking = Blueprint('banking', __name__)


# home page for everyone
@banking.route('/')
def index():
    return render_template("index.html")

# home page for loged in users that will show data 
@banking.route('/home')
def home():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    user_data = Storage.load_data(session["username"])
    name = user_data.get("name")
    balance = user_data.get("balance")
    transactions = user_data.get("transactions", [])
    return render_template("home.html", balance=balance, transactions=transactions, username=session["username"], name=name)

@banking.route('/transactions', methods=['GET'])
def transactions():
    if not session.get("user_id"): 
        return redirect(url_for("auth.login"))
    
@banking.route('/transfer', methods=['GET', 'POST'])
def transfer():
    return "transfer page"

@banking.route('/bills', methods=['GET', 'POST'])
def bills():
    return "bills page"

@banking.route('/settings', methods=['GET', 'POST'])
def settings():
    return "settings page"


@banking.route('/accounts', methods=['GET', 'POST'])
def accounts():
    return "accounts page"