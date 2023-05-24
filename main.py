from flask import Flask, request, jsonify
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
storage = firebase.storage()

app = Flask(__name__)

# GET /hotels - Returns a list of all hotels
@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = db.child('hotels').get().val()
    return jsonify(hotels)

# GET /hotels/{hotel_id} - Returns details for a specific hotel
@app.route('/hotels/<hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = db.child('hotels').child(hotel_id).get().val()
    if hotel:
        return jsonify(hotel)
    else:
        return jsonify({'message': 'Hotel not found'})

# POST /hotels - Creates a new hotel with the provided details
@app.route('/hotels', methods=['POST'])
def create_hotel():
    data = request.json
    new_hotel = db.child('hotels').push(data)
    if new_hotel:
        return jsonify({'message': 'Hotel created successfully', 'hotel_id': new_hotel.key()})
    else:
        return jsonify({'message': 'Failed to create hotel'})

# PUT /hotels/{hotel_id} - Updates the details for a specific hotel
@app.route('/hotels/<hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    data = request.json
    db.child('hotels').child(hotel_id).update(data)
    return jsonify({'message': 'Hotel updated successfully'})

# DELETE /hotels/{hotel_id} - Deletes a specific hotel
@app.route('/hotels/<hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    db.child('hotels').child(hotel_id).remove()
    return jsonify({'message': 'Hotel deleted successfully'})

# GET /hotels/{hotel_id}/rooms - Returns a list of all rooms for a specific hotel
@app.route('/hotels/<hotel_id>/rooms', methods=['GET'])
def get_rooms(hotel_id):
    rooms = db.child('hotels').child(hotel_id).child('rooms').get().val()
    if rooms:
        return jsonify(rooms)
    else:
        return jsonify({'message': 'Rooms not found'})

# GET /hotels/{hotel_id}/rooms/{room_id} - Returns details for a specific room in a specific hotel
@app.route('/hotels/<hotel_id>/rooms/<room_id>', methods=['GET'])
def get_room(hotel_id, room_id):
    room = db.child('hotels').child(hotel_id).child('rooms').child(room_id).get().val()
    if room:
        return jsonify(room)
    else:
        return jsonify({'message': 'Room not found'})

# POST /hotels/{hotel_id}/rooms - Creates a new room for a specific hotel with the provided details
@app.route('/hotels/<hotel_id>/rooms', methods=['POST'])
def create_room(hotel_id):
    data = request.json
    new_room = db.child('hotels').child(hotel_id).child('rooms').push(data)
    if new_room:
        return jsonify({'message': 'Room created successfully', 'room_id': new_room.key()})
    else:
        return jsonify({'message': 'Failed to create room'})

# PUT /hotels/{hotel_id}/rooms/{room_id} - Updates the details for a specific room in a specific hotel
@app.route('/hotels/<hotel_id>/rooms/<room_id>', methods=['PUT'])
def update_room(hotel_id, room_id):
    data = request.json
    db.child('hotels').child(hotel_id).child('rooms').child(room_id).update(data)
    return jsonify({'message': 'Room updated successfully'})

# DELETE /hotels/{hotel_id}/rooms/{room_id} - Deletes a specific room in a specific hotel
@app.route('/hotels/<hotel_id>/rooms/<room_id>', methods=['DELETE'])
def delete_room(hotel_id, room_id):
    db.child('hotels').child(hotel_id).child('rooms').child(room_id).remove()
    return jsonify({'message': 'Room deleted successfully'})


if __name__ == '__main__':
    app.run()
