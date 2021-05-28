from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource, request, reqparse

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/todoapp"
mongo = PyMongo(app)
api = Api(app)

users_collection = mongo.db.users

class tasks(Resource):
    def get(self, username):
        user = users_collection.find_one({"name": username})
        user['_id'] = str(user['_id'])
        return jsonify(user)

    def post(self, username):
        req = request.get_json()
        user = list(users_collection.find({"name": username}))

        if user == []: 
            return jsonify({"message":'failed. task was not added', "status":400})
        
        users_collection.find_one_and_update({"name": username}, {"$push":{"tasks":req["task"]}})
        return jsonify({"message": "task added", "status": 200})
    
    def delete(self, username):
        req = request.get_json()

        user = users_collection.find_one({"name": username})
        user['tasks'] = [task for task in user['tasks'] if task != req['task']]
        users_collection.find_one_and_update({"name": username}, {"$set": {"tasks": user['tasks']}})
        return jsonify(user['tasks'])
         
api.add_resource(tasks, '/tasks/', "/tasks/<username>")

class UsersList(Resource):
    def get(self):
        users = list(users_collection.find({}))
        users2=[]
        for user in users:
            user['_id'] = str(user['_id'])
            users2.append(user)

        return jsonify(users2)

    def post(self):
        req = request.get_json()
        new_user = insert_user(req["name"])
        return jsonify(new_user)
        

api.add_resource(UsersList, '/users/')


def insert_user(username):
    user = list(users_collection.find({"name": username}))
    if user: 
        return {"message":'username already in use', "status":400}
    
    users_collection.insert_one({"name": username, "tasks": []})
    return {"message":'user created', "status":200}


if __name__ == '__main__':
    app.run(debug=True)
