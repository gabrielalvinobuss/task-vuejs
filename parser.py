import json
from pymongo import MongoClient
from dataclasses import dataclass
from typing import List
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, 'udata.json')

@dataclass
class UserPreferences:
    def __init__(self, timezone):
        self.timezone = timezone

    def to_dict(self):
        return {
            'timezone': self.timezone
        }

@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    active: bool
    created_ts: float

def parse_roles(user_data):
    roles = []
    if user_data.get("is_user_admin"):
        roles.append("admin")
    if user_data.get("is_user_manager"):
        roles.append("manager")
    if user_data.get("is_user_tester"):
        roles.append("tester")
    return roles

# MongoDB credentials
username = 'dev_admin'
password = 'test'
cluster = 'cluster0'
dbname = 'task'
collection_name = 'user'

# MongoDB URL
url = f"mongodb+srv://{username}:{password}@{cluster}.i8ffi.mongodb.net/{dbname}?retryWrites=true&w=majority&appName={cluster}"

# MongoDB connection
def connect_to_db():
    client = MongoClient(url)
    db = client[dbname]
    return db["users"]

# import data from JSON file
def import_data():

    with open(json_file_path) as f:
        data = json.load(f)

    users_collection = connect_to_db()

    imported_users_count = 0
    for user_data in data['users']:
        user = User(
            username = user_data["user"],
            password = user_data["password"],
            roles = parse_roles(user_data),
            preferences = UserPreferences(timezone=user_data["user_timezone"]),
            active = user_data["is_user_active"],
            created_ts = datetime.strptime(user_data["created_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        )
        
        user_dict = user.__dict__.copy()
        user_dict['preferences'] = user.preferences.to_dict()

        # MongoDB insert
        users_collection.insert_one(user_dict)
        imported_users_count += 1
    
        print(f"{imported_users_count} users imported")

if __name__ == "__main__":
    import_data()