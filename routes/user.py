# routes/user.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import get_db

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, nom, prenom, email, tel, profession, active
        FROM personne WHERE id=%s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return jsonify(msg="Profil non trouvé"), 404
    keys = ['id','nom','prenom','email','tel','profession','active']
    return jsonify(dict(zip(keys, row))), 200

@user_bp.route('/update/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    allowed = ('nom','prenom','email','tel','profession')
    fields = {k: data[k] for k in allowed if k in data}
    if not fields:
        return jsonify(msg="Aucun champ à mettre à jour"), 400

    set_clause = ', '.join(f"{k}=%s" for k in fields)
    params = list(fields.values()) + [user_id]

    db  = get_db()
    cur = db.cursor()
    cur.execute(f"UPDATE personne SET {set_clause} WHERE id=%s", params)
    db.commit()
    cur.close()

    return jsonify(msg="Profil mis à jour"), 200

@user_bp.route('/profile/desactive', methods=['PUT'])
@jwt_required()
def toggle_active():
    user_id = get_jwt_identity()
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT active FROM personne WHERE id=%s", (user_id,))
    current = cur.fetchone()
    if not current:
        cur.close()
        return jsonify(msg="Utilisateur non trouvé"), 404
    new_state = 0 if current[0] else 1
    cur.execute("UPDATE personne SET active=%s WHERE id=%s", (new_state, user_id))
    db.commit()
    cur.close()
    return jsonify(msg="Statut modifié", active=bool(new_state)), 200
