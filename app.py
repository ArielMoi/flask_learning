from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_pymongo import PyMongo
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/todoapp"
mongo = PyMongo(app)

collection_users = mongo.db.users

@app.route('/')
def front():
    return 'react app here'

@app.route('/create/<user>', methods=['GET', 'POST'])
def create(user):
    print(request)
    # collection_users.insert_one({"name": user, "tasks":{}})
    return 'create' + user

if __name__ == '__main__':
    app.run(debug=True)
