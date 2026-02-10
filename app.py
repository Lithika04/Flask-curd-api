
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database (list of dictionaries)
users = []
user_id_counter = 1

# -----------------------
# CREATE (POST)
# -----------------------
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter

    data = request.get_json()

    if not data or not data.get('name') or not data.get('email'):
        return jsonify({
            "error": "Name and email are required"
        }), 400

    user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data['email']
    }

    users.append(user)
    user_id_counter += 1

    return jsonify({
        "message": "User created successfully",
        "user": user
    }), 201


# -----------------------
# READ ALL (GET)
# -----------------------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


# -----------------------
# READ ONE (GET)
# -----------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user), 200

    return jsonify({
        "error": "User not found"
    }), 404


# -----------------------
# UPDATE (PUT)
# -----------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    for user in users:
        if user['id'] == user_id:
            user['name'] = data.get('name', user['name'])
            user['email'] = data.get('email', user['email'])

            return jsonify({
                "message": "User updated successfully",
                "user": user
            }), 200

    return jsonify({
        "error": "User not found"
    }), 404


# -----------------------
# DELETE (DELETE)
# -----------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({
                "message": "User deleted successfully"
            }), 200

    return jsonify({
        "error": "User not found"
    }), 404


if __name__ == '__main__':
    app.run(debug=True)
