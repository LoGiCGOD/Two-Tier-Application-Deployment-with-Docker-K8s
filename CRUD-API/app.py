from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import os

app = Flask(__name__)


# Use Kubernetes Secrets to get MongoDB credentials
mongo_username = os.environ.get('MONGO_USERNAME', 'default_username')
mongo_password = os.environ.get('MONGO_PASSWORD', 'default_password')


# MongoDB configuration
app.config['MONGO_URI'] = f'mongodb://{mongo_username}:{mongo_password}@mongo-service.db.svc.cluster.local:27017/usersdb'
mongo = PyMongo(app)

# Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'username': user['username'],
            'password': user['password']
        })
    return jsonify(result)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        result = {
            'id': str(user['_id']),
            'username': user['username'],
            'password': user['password']
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user_id = mongo.db.users.insert_one({'username': username, 'password': password})
        return jsonify({'id': str(user_id)}), 201
    else:
        return jsonify({'error': 'Username and password are required'}), 400

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'username': username, 'password': password}}
        )
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Username and password are required'}), 400

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
