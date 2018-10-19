from flask import Flask
from flask_restful import Api
from .resources import HashtagAPI, HashtagListAPI

# from flask_pymongo import PyMongo

# initialize api
app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# api = PyMongo(app)
api = Api(app)

# add api resources
api.add_resource(HashtagListAPI, "/api/v1.0/hashtags", endpoint="hashtags")
api.add_resource(HashtagAPI, "/api/v1.0/hashtags/<int:id>", endpoint="hashtag")

if __name__ == "__main__":
    app.run(debug=True)
