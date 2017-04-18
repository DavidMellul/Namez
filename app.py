import json
from json import JSONDecodeError
from flask import Flask, jsonify, request, abort

app = Flask(__name__)


@app.route('/')
def index_handler():
    return "Welcome to Namez."


# Insert a new name into the database
@app.route('/names', methods=['POST'])
def create_handler():
    # First, check if the request contains JSON
    if request.json is None:
        abort(400)

    # Then, look if the JSON content has got the key "name"
    if request.json['name'] is None:
        abort(400)

    name = str(request.json['name']).upper()

    # In the end, check if the name doesn't exist already
    if name in names:
        abort(409)

    # Insert the new name
    names.append(name)
    save_data()
    return jsonify({'name': name}), 201


# Retrieve all the names from the database
@app.route('/names', methods=['GET'])
def read_handler():
    return jsonify({'names': names}), 200


# Update an existing name
@app.route('/names/<old_name>', methods=['PUT'])
def update_handler(old_name):
    old_name = str(old_name).upper()

    # First, check if the request contains JSON
    if request.json is None:
        abort(400)

    # Then, look if the JSON content has got the key "name"
    if request.json['name'] is None:
        abort(400)

    new_name = str(request.json['name']).upper()

    # In the end, check if the name exists already
    if old_name not in names:
        abort(404)

    # Update the old name with the new one
    names[names.index(old_name)] = new_name
    save_data()
    return jsonify({'name': new_name}), 200


# Delete an existing name
@app.route('/names/<name>', methods=['DELETE'])
def delete_handler(name):
    name = str(name).upper()
    # First, check if the name exists in the database
    if name not in names:
        abort(404)

    # Delete the requested name
    names.remove(name)
    save_data()
    return jsonify({'name': name}), 204


# Make all the data persistent by storing it into data.json
def save_data():
    try:
        names.sort()
        with open('data.json', 'w') as out_file:
            json.dump({'names': names}, out_file)
    except FileNotFoundError:
        pass


# Do not start the server in case this script is imported into an other
if __name__ == '__main__':
    # List containing all the names
    names = list()
    # List containing all the api keys required to communicate with the API
    keys = list()

    # If possible, retrieve what once has been stored
    try:
        with open('data.json', 'r') as in_file:
            names = sorted(json.load(in_file)['names'])
            keys = sorted(json.load(in_file)['keys'])
    except (FileNotFoundError, JSONDecodeError):
        pass

    # Start the Flask server
    app.run(host="127.0.0.1", port=8080)
