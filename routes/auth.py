# routes/auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.db import get_db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required = ('lastname','firstname','sexe','birthday','work','email','user','password')
    if not all(k in data for k in required):
        return jsonify(msg="Champs manquants"), 400

    pwd_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO personne
            (nom, prenom, sexe, date_naissance, profession, email, username, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['lastname'], data['firstname'], data['sexe'],
            data['birthday'], data['work'],
            data['email'], data['user'], pwd_hash
        ))
        db.commit()
    except Exception as e:
        return jsonify(msg="Erreur SQL", error=str(e)), 500
    finally:
        cur.close()

    return jsonify(msg="Utilisateur créé"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify(msg="Email et mot de passe requis"), 400

    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, password, active FROM personne WHERE email=%s", (data['email'],))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify(msg="Utilisateur non trouvé"), 404
    user_id, pwd_hash, active = row
    if not active:
        return jsonify(msg="Compte désactivé"), 403

    if not bcrypt.checkpw(data['password'].encode(), pwd_hash.encode()):
        return jsonify(msg="Mot de passe incorrect"), 401

    token = create_access_token(identity=str(user_id))
    return jsonify(access_token=token), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify(msg="Déconnexion réussie"), 200
