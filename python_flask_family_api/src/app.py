"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"family": members}
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_individual(id):
    member = jackson_family.get_member(id)
    print(member)
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def add_new_member():
    request_body = request.json
    response = jackson_family.add_member(request_body)
    print("Incoming request with the following body", request_body)
    return jsonify(response), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    response = jackson_family.delete_member(id)
    print("Deleted item: ", response)
    return jsonify(response), 200

@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    print("This is the position to delete:", position, "and the item:", todos[position])
    del todos[position]
    json_todos = jsonify(todos)
    return json_todos

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
