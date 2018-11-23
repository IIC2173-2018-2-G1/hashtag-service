import os
import json
from datetime import datetime
from flask import Flask, request
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_restful import (Resource, reqparse, fields, marshal)
from bson import ObjectId
from pymongo import UpdateOne

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("DB")
MONGO = PyMongo(app)

hashtag_parser = reqparse.RequestParser()
hashtag_parser.add_argument("hashtag", required=True)

hashtag_fields = {"id": fields.String, "name": fields.String}


def marshall_hashtag(hashtag):
    return str(hashtag["name"])


class HashtagListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "hashtags",
            type=list,
            required=True,
            help="No hashtags provided",
            location="json",
        )
        self.reqparse.add_argument(
            "message_id",
            type=str,
            required=True,
            help="No message id provided",
            location="json",
        )
        super(HashtagListAPI, self).__init__()

    def get(self):
        hashtags = MONGO.db.hashtags.find().sort("name")
        return [marshall_hashtag(hashtag) for hashtag in hashtags]

    def post(self):
        message_id = self.reqparse.parse_args()["message_id"]
        hashtags = request.json["hashtags"]
        operations = [UpdateOne({"name": name}, {"$push": {"messages": message_id}}, upsert=True) for name in hashtags]
        MONGO.db.hashtags.bulk_write(operations)
        return hashtags, 201


api = Api(app)

# add api resources
api.add_resource(HashtagListAPI, "/", endpoint="hashtags")

if __name__ == "__main__":
    app.run(debug=True)
