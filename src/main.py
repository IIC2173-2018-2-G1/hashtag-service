import os
import json
from datetime import datetime
from flask import Flask, request
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_restful import (Resource, reqparse, fields, marshal)
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("DB")
MONGO = PyMongo(app)

hashtag_parser = reqparse.RequestParser()
hashtag_parser.add_argument("hashtag", required=True)

hashtag_fields = {"_id": fields.String, "name": fields.String,
                  "user_id": fields.String, "created_at": fields.DateTime,
                  "updated_at": fields.DateTime, "uri": fields.Url('hashtag')}


def get_user_id():
    json_obj = json.loads(request.headers.get('current-user'))
    return json_obj["_id"]


class HashtagListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            type=str,
            required=True,
            help="No hashtag name provided",
            location="json",
        )
        self.reqparse.add_argument("current-user", required=True,
                                   help="No user provided", location="headers")
        super(HashtagListAPI, self).__init__()

    def get(self):
        _data = MONGO.db.hashtags.find()
        hashtags = [hashtag for hashtag in _data]
        return {'hashtags': [marshal(hashtag, hashtag_fields)
                             for hashtag in hashtags]}

    def post(self):
        args = self.reqparse.parse_args()
        user_id = get_user_id()
        now = datetime.now()
        hashtag = {"name": args["name"], "user_id": user_id,
                   "created_at": now, "updated_at": now}
        MONGO.db.hashtags.insert_one(hashtag)
        _last_added = MONGO.db.hashtags.find().sort([("$natural", -1)]).limit(1)
        last_added = [hashtag for hashtag in _last_added]
        return {'hashtag': [marshal(hashtag, hashtag_fields)
                            for hashtag in last_added]}, 201


class HashtagAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        super(HashtagAPI, self).__init__()

    def get(self, _id):
        object_id = ObjectId(_id)
        hashtag = MONGO.db.hashtags.find_one_or_404({"_id": object_id})
        return {"hashtag": marshal(hashtag, hashtag_fields)}


api = Api(app)

# add api resources
api.add_resource(HashtagListAPI, "/", endpoint="hashtags")
api.add_resource(HashtagAPI, "/<string:_id>",
                 endpoint="hashtag")

if __name__ == "__main__":
    app.run(debug=True)
