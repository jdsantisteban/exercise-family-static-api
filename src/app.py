"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Get all family members:
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "world",
    #     "family": members
    # }

    return jsonify(members), 200

# 2) Retrieve one member
@app.route('/member/<int:member_id>', methods=["GET"])
def get_member(member_id=None):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({'message':"member doesn't exist"}), 400
    
    new_member = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }
    return jsonify(new_member), 200

# 3) Add (POST) new member
@app.route('/member', methods=['POST'])
def new_member():
    request_body = request.get_json()
   
    member = {
        "id": jackson_family._generateId(),
        "first_name": request_body.get("first_name"),
        "age": request_body.get("age"),
        "lucky_numbers": request_body.get("lucky_numbers")
    }
    
    jackson_family.add_member(member)

    return jsonify({"message": "New member added"}), 200

# 4) DELETE one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id=None):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({'message':"member doesn't exist"}), 400
    else:
        jackson_family.delete_member(member_id)
        return jsonify({"message": "A member was deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
