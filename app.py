from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB credentials
username = 'dev_admin'
password = 'test'
cluster = 'cluster0'
dbname = 'task'
collection_name = 'user'

# MongoDB URL
url = f"mongodb+srv://{username}:{password}@{cluster}.i8ffi.mongodb.net/{dbname}?retryWrites=true&w=majority&appName={cluster}"

# MongoDB connection
client = MongoClient(url)
db = client[dbname]
users_collection = db["users"]

# List all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    return jsonify(users)

# Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.json
    users_collection.insert_one(user_data)
    return jsonify({"message": "User created successfully"})

# Edit a user
@app.route('/api/users/<username>', methods=['PUT'])
def update_user(username):
    user_data = request.json
    users_collection.update_one({"username": username}, {"$set": user_data})
    return jsonify({"message": "User updated successfully"})

# Delete a user
@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    users_collection.delete_one({"username": username})
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug = True)
