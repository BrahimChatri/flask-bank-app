from flask import Flask, jsonify
from views.banking import banking
from views.auth import auth
from views.admin import admin
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_object('config.Config')
mail = Mail(app)

app.register_blueprint(banking, url_prefix='/banking')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error":" the page you looking for not found"}), 404

if __name__=='__main__':
    app.run(port="5000", debug=True, host="0.0.0.0")