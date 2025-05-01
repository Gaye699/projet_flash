# app.py

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from models.db import close_db   # Ajout pour fermer la connexion après chaque requête
from routes.auth import auth_bp
from routes.user import user_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Enregistre la fonction close_db à la fin de chaque requête Flask
app.teardown_appcontext(close_db)

# Init JWT
jwt = JWTManager(app)

# Enregistre les blueprints avec leurs préfixes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    return jsonify(msg="Auth API is running"), 200

if __name__ == '__main__':
    app.run(debug=True)
