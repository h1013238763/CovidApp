from flask import Blueprint, jsonify, request, redirect

API = Blueprint('API', __name__)


VALID_USERNAME = 'admin'
VALID_PASSWORD = 'password'


@API.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("username") == VALID_USERNAME and data.get("password") == VALID_PASSWORD:
        return jsonify(userAuthenticated="true"), 200

@API.route('/api/create_account', methods=['POST'])
def create_count():
    data = request.get_json()
<<<<<<< HEAD
    if data.get("username") in in_memory_user_dictionary:
        return jsonify(userAuthenticated="false", error_mes="user already exist...login."), 200
    else:
        in_memory_user_dictionary[data.get("username")] = {'password': data.get("password"), 'email': data.get("email")}
        print(in_memory_user_dictionary)
=======
    if data.get("username") == VALID_USERNAME and data.get("password") == VALID_PASSWORD:
>>>>>>> parent of 8732299 (Prototype 1 Complete and all function been tested)
        return jsonify(userAuthenticated="true"), 200

        
#create "crate account endpoint"
#create "reset password" -> prototype 2





if __name__ == '__main__':
    app.run(debug=True)
