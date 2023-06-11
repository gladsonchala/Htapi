from flask import Flask, Response, request, jsonify
import json
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)

# Connecting with MongoDB database
try:
    mongo_uri = "mongodb://username:password@localhost:27017/?authSource=admin"
    mongo = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
    mongo.server_info()  # Trigger exception if cannot connect to database
    db = mongo.hotelify
except:
    print("ERROR - Cannot connect to database")


# Get all hotels
@app.route("/hotels", methods=["GET"])
def get_hotels():
    try:
        hotels = list(db.hotels.find())
        for hotel in hotels:
            hotel["_id"] = str(hotel["_id"])
        return Response(
            response=json.dumps(hotels),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error fetching hotels"}),
            status=500,
            mimetype="application/json"
        )


# Get a hotel by ID
@app.route("/hotels/<hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    try:
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if hotel:
            hotel["_id"] = str(hotel["_id"])
            return Response(
                response=json.dumps(hotel),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error fetching a hotel"}),
            status=500,
            mimetype="application/json"
        )


# Create a hotel
@app.route("/hotels", methods=["POST"])
def create_hotel():
    try:
        hotel_data = request.get_json()
        hotel = {
            "name": hotel_data["name"],
            "photos_url": hotel_data["photos_url"],
            "ground": hotel_data["ground"],
            "city": hotel_data["city"],
            "approximate_location": hotel_data["approximate_location"],
            "google_map_location_url": hotel_data["google_map_location_url"],
            "latitude": hotel_data["latitude"],
            "longitude": hotel_data["longitude"],
            "price_range": hotel_data["price_range"],
            "additional_services": hotel_data["additional_services"],
            "rooms": [],
            "other_description": hotel_data["other_description"]
        }

        dbResponse = db.hotels.insert_one(hotel)
        return Response(
            response=json.dumps(
                {"message": "Hotel created", "id": str(dbResponse.inserted_id)}
            ),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error creating a hotel"}),
            status=500,
            mimetype="application/json"
        )


# Update a hotel
@app.route("/hotels/<hotel_id>", methods=["PUT"])
def update_hotel(hotel_id):
    try:
        hotel_data = request.get_json()
        updated_hotel = {
            "name": hotel_data["name"],
            "photos_url": hotel_data["photos_url"],
            "ground": hotel_data["ground"],
            "city": hotel_data["city"],
            "approximate_location": hotel_data["approximate_location"],
            "google_map_location_url": hotel_data["google_map_location_url"],
            "latitude": hotel_data["latitude"],
            "longitude": hotel_data["longitude"],
            "price_range": hotel_data["price_range"],
            "additional_services": hotel_data["additional_services"],
            "other_description": hotel_data["other_description"]
        }

        dbResponse = db.hotels.update_one(
            {"_id": ObjectId(hotel_id)},
            {"$set": updated_hotel}
        )

        if dbResponse.modified_count > 0:
            return Response(
                response=json.dumps({"message": "Hotel updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error updating a hotel"}),
            status=500,
            mimetype="application/json"
        )


# Delete a hotel
@app.route("/hotels/<hotel_id>", methods=["DELETE"])
def delete_hotel(hotel_id):
    try:
        dbResponse = db.hotels.delete_one({"_id": ObjectId(hotel_id)})

        if dbResponse.deleted_count > 0:
            return Response(
                response=json.dumps({"message": "Hotel deleted"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error deleting a hotel"}),
            status=500,
            mimetype="application/json"
        )


# Get all rooms of a hotel
@app.route("/hotels/<hotel_id>/rooms", methods=["GET"])
def get_rooms(hotel_id):
    try:
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if hotel:
            rooms = hotel["rooms"]
            return Response(
                response=json.dumps(rooms),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error fetching rooms"}),
            status=500,
            mimetype="application/json"
        )


# Get a room by ID
@app.route("/hotels/<hotel_id>/rooms/<room_id>", methods=["GET"])
def get_room(hotel_id, room_id):
    try:
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if hotel:
            rooms = hotel["rooms"]
            room = next(
                (item for item in rooms if item["room_id"] == room_id), None
            )
            if room:
                return Response(
                    response=json.dumps(room),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Room not found"}),
                    status=404,
                    mimetype="application/json"
                )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error fetching a room"}),
            status=500,
            mimetype="application/json"
        )


# Create a room for a hotel
@app.route("/hotels/<hotel_id>/rooms", methods=["POST"])
def create_room(hotel_id):
    try:
        room_data = request.get_json()
        room = {
            "room_id": room_data["room_id"],
            "room_type": room_data["room_type"],
            "room_area": room_data["room_area"],
            "room_pricing": room_data["room_pricing"],
            "room_photos": room_data["room_photos"],
            "additional_services": room_data["additional_services"],
            "other_description": room_data["other_description"]
        }

        dbResponse = db.hotels.update_one(
            {"_id": ObjectId(hotel_id)},
            {"$push": {"rooms": room}}
        )

        if dbResponse.modified_count > 0:
            return Response(
                response=json.dumps({"message": "Room created"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Hotel not found"}),
                status=404,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error creating a room"}),
            status=500,
            mimetype="application/json"
        )


# Update a room
@app.route("/hotels/<hotel_id>/rooms/<room_id>", methods=["PUT"])
def update_room(hotel_id, room_id):
    try:
        room_data = request.get_json()
        updated_room = {
            "room_type": room_data["room_type"],
            "room_area": room_data["room_area"],
            "room_pricing": room_data["room_pricing"],
            "room_photos": room_data["room_photos"],
            "additional_services": room_data["additional_services"],
            "other_description": room_data["other_description"]
        }

        dbResponse = db.hotels.update_one(
            {"_id": ObjectId(hotel_id), "rooms.room_id": room_id},
            {"$set": {"rooms.$": updated_room}}
        )

        if dbResponse.modified_count > 0:
            return Response(
                response=json.dumps({"message": "Room updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Room not found"}),
                status=404,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error updating a room"}),
            status=500,
            mimetype="application/json"
        )


# Delete a room
@app.route("/hotels/<hotel_id>/rooms/<room_id>", methods=["DELETE"])
def delete_room(hotel_id, room_id):
    try:
        dbResponse = db.hotels.update_one(
            {"_id": ObjectId(hotel_id)},
            {"$pull": {"rooms": {"room_id": room_id}}}
        )

        if dbResponse.modified_count > 0:
            return Response(
                response=json.dumps({"message": "Room deleted"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "Room not found"}),
                status=404,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error deleting a room"}),
            status=500,
            mimetype="application/json"
        )


# Search hotels
@app.route("/hotels/search", methods=["GET"])
def search_hotels():
    query = request.args.get("query")
    try:
        hotels = list(
            db.hotels.find(
                {"$or": [{"name": {"$regex": query, "$options": "i"}},
                         {"city": {"$regex": query, "$options": "i"}}]}
            )
        )

        for hotel in hotels:
            hotel["_id"] = str(hotel["_id"])

        return Response(
            response=json.dumps(hotels),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Error searching hotels"}),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(debug=True)
