import json
from json import JSONDecodeError
from bottle import request, response
from bottle import post, get, put, delete
from bottle import abort
from bottle import run


# Insert a new element
@post('/names')
def create_handler():
    if not request_contains_json():
        abort(400, "Bad request, please use well-formatted JSON")

    to_add = str(request.json['name']).upper()

    if to_add in names:
        abort(409, "This name already exists.")

    names.append(to_add)
    update_database_content()


# List all the existing elements
@get('/names')
def read_handler():
    response.headers['Content-Type'] = 'application/json'
    data = json.dumps({'names': names})
    return data


# Modify an existing element
@put('/names/<name>')
def update_handler(to_change):
    to_change = str(to_change).upper()

    if not request_contains_json():
        abort(400, "Bad request, please use well-formatted JSON")

    new_one = str(request.json['name']).upper()

    if to_change not in names:
        abort(404, "Name not found.")

    names[names.index(to_change)] = new_one
    update_database_content()


# Delete an existing element
@delete('/names/<name>')
def delete_handler(name):
    name = str(name).upper()
    if str(name).upper() in names:
        names.remove(name)
        update_database_content()
    else:
        abort(404, "Name not found.")


# Tells whether the request contains a JSON content
def request_contains_json():
    return request.headers['Content-Type'] == 'application/json'


# Fill the file responsible for storing all the data. It's used the same way a .db file is used
def update_database_content():
    try:
        with open('data.json', 'w') as out_file:
            json.dump({'names': names}, out_file, indent=4)
    except FileNotFoundError:
        pass


# This condition is useful so that if one imports this script, it won't run automatically
if __name__ == '__main__':
    names = list()
    keys = list()

    # If it exists, load the file responsible for storing everything (database-like)
    try:
        with open('data.json', 'r') as in_file:
            names = json.load(in_file)['names']
            keys = json.load(in_file)['keys']
    except (FileNotFoundError,JSONDecodeError):
        pass

    run(host="localhost", port=8080)
