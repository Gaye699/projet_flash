# from django.apps import AppConfig
from app import app, db 
from models import User, Room  
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import jwt



@app.route('/create_room', methods=['POST'])
@jwt_required()
def create_room():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user:
        data = request.json
        room_name = data.get('name')

        if room_name:
            # Créez une nouvelle salle dans la base de données
            new_room = Room(name=room_name)
            db.session.add(new_room)
            db.session.commit()

            return jsonify({'message': 'Room created successfully'}), 201
        else:
            return jsonify({'error': 'Room name is required'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404
    

@app.route('/join_room', methods=['POST'])
@jwt_required()
def join_room():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user:
        data = request.json
        room_id = data.get('room_id')

        if room_id:
            # Vérifiez si la salle existe
            room = Room.query.filter_by(id=room_id).first()
            if room:
                # Ajoutez l'utilisateur à la salle de discussion
                room.users.append(user)
                db.session.commit()

                return jsonify({'message': 'User joined the room successfully'}), 200
            else:
                return jsonify({'error': 'Room not found'}), 404
        else:
            return jsonify({'error': 'Room ID is required'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404
    


@app.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user:
        data = request.json
        room_id = data.get('room_id')
        message_content = data.get('message')

        if room_id and message_content:
            # Vérifiez si la salle existe
            room = Room.query.filter_by(id=room_id).first()
            if room:
                # Créez un nouvel objet Message
                message = Message(author=user, content=message_content, room=room)
                db.session.add(message)
                db.session.commit()

                return jsonify({'message': 'Message sent successfully'}), 200
            else:
                return jsonify({'error': 'Room not found'}), 404
        else:
            return jsonify({'error': 'Room ID and message content are required'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404