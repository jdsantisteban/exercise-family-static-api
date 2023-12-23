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

    members = jackson_family.get_all_members()

    return jsonify(members), 200

# 2) Retrieve one member
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        return jsonify(member), 200
    except Exception as error:
        return jsonify({"message": f"error: {error.args}"}), 500
    
# 3) Add (POST) new member
@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_body = request.get_json()
        required_fields = ['id', 'first_name','age', 'lucky_numbers']

        if not all(field in request_body for field in required_fields):
            return jsonify({'message': 'Missing fields'}), 400

        new_member = {
            "id": request_body['id'],
            "first_name": request_body['first_name'],
            "age": request_body['age'],
            "lucky_numbers": request_body["lucky_numbers"]
        }

        jackson_family.add_member(new_member)
        return jsonify({"message": "New member added"}), 200
    except Exception as error:
        return jsonify({"message": f"error: {error.args}"}), 500

# 4) DELETE one member
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id=None):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({'message':"member doesn't exist"}), 400
    else:
        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
