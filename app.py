from flask import Flask, render_template
from views.banking import banking
from views.auth import auth
from dotenv import load_dotenv
import os
from datetime import timedelta


load_dotenv()

app = Flask(__name__)
app.register_blueprint(banking, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
KEY = os.getenv("KEY")

app.config['SECRET_KEY'] = KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__=='__main__':
    app.run(port="5000", debug=True, host="0.0.0.0")