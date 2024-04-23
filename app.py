from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
#from flaskext.mysql import MySQL
from chat import create_room
import json
import math
import jwt
import bcrypt
import pymysql


app = Flask(__name__)
#mysql = MySQL(app)
app.config['JWT_SECRET_KEY'] = 'info2-security'
jwt = JWTManager(app)   



# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'user_auth_sql'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#mysql.init_app(app)
@app.route('/', methods=['GET'])
def hello_world():
   
    
    return jsonify('hello world')



def get_connection_db():
    
    try:
        db = pymysql.connect(
        user='root',
        password='',
        db='user_auth_sql',
        host='localhost'
        )
        return db
    except OperationalError as e:
        print(e)
        return None
    
# Route d'enregistrement
@app.route('/register', methods=['POST'])
def register():
    nom = request.json.get('lastname')
    prenom = request.json.get('firstname')
    sexe = request.json.get('sexe')
    date_naissance = request.json.get('birthday')
    username = request.json.get('user')
    email = request.json.get('email')
    password = request.json.get('password')
    active = True

    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Enregistrement de l'utilisateur dans la base de données
    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO personne(nom,prenom,date_naissance,sexe,email,nom_utilisateur,mot_de_passe,active) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)", (nom, prenom, sexe, date_naissance, email, username,hashed_password, active))
    connection.commit()
    cursor.close()

    return jsonify({'message': 'Personne registered successfully'})


# Route de connexion
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Récupération de l'utilisateur depuis la base de données
    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, password FROM personne WHERE email = %s", (email,))
    user = cursor.fetchone()
    identifiantGet = user[0]
    passwordGet = user[1]
    cursor.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), passwordGet.encode('utf-8')):
        # Génération du token JWT
        access_token = create_access_token(identity=identifiantGet)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# Route de profil utilisateur
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (current_user_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns[:-2], cursor.fetchone()[:-2]))
    cursor.close()

    if users_details:
        return jsonify({'profile':users_details}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

#Route de modification de profile
@app.route('/update/profile', methods=['PUT'])
@jwt_required()
def update():
    current_user_id = get_jwt_identity()
    nom = request.json.get('lastname')
    prenom = request.json.get('firstname')
    sexe = request.json.get('sexe')
    date_naissance = request.json.get('birthday')
    profession = request.json.get('work')
    username = request.json.get('user')
    email = request.json.get('email')
    password = request.json.get('password')
    active = True

    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE personne SET nom=%s, prenom=%s, sexe=%s, date_naissance=%s,profession=%s, email=%s, username=%s WHERE id=%s", (nom, prenom, sexe, date_naissance,profession, email, username, current_user_id))
    connection.commit()
    cursor.close()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (current_user_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns[:-2], cursor.fetchone()[:-2]))

    return jsonify({'message': 'Profile updated successfully', 'data': users_details})

#Route d'activation/desactivation de profile
@app.route('/profile/desactive', methods=['PUT'])
@jwt_required()
def desactivate():
    username_id = request.json.get('user')
    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (username_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns, cursor.fetchone()))
    active = users_details["active"]
    message = ""
    if(active == True):
        active = False
        message = "Profile desactivated successfully"
    else:
        active = True
        message = "Profile activated successfully"
    cursor = connection.cursor()
    cursor.execute("UPDATE personne SET active=%s WHERE id=%s", (active, username_id))
    connection.commit()
    cursor.close()

    return jsonify({'message': message, 'data': users_details})

# Route de déconnexion (inutile pour les tokens JWT)
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run()




#Devoir faire une calculatrice simple

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello_world():
#     return jsonify({'message': 'Bienvenu dans la calulatrice API!'})

# @app.route('/calculate', methods=['GET'])
# def calculate():
#     num1 = request.args.get('num1', type=int)
#     num2 = request.args.get('num2', type=int)
#     operator = request.args.get('operator', type=str)

#     if num1 is None or num2 is None or operator is None:
#         return jsonify({'error': 'Missing parameters!'}), 400

#     if operator == '+':
#         result = num1 + num2
#     elif operator == '-':
#         result = num1 - num2
#     elif operator == '*':
#         result = num1 * num2
#     elif operator == '/':
#         if num2 == 0:
#             return jsonify({'error': 'Division par zero non impossible!'}), 400
#         result = num1 / num2
#     elif operator == '^':
#         result = num1 ** num2
#     elif operator == '!':
#         result = math.factorial(num1)
#     elif operator == 'sqrt':
#         result = num1 ** (1/num2)
#     else:
#         return jsonify({'erreur': 'Operation invalide!'}), 400

#     return jsonify({'resultat': result})

# if __name__ == '__main__':
#     app.run(debug=True)

# #faire le tp2 