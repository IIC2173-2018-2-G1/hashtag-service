from flask_restful import Resource, reqparse, abort, fields, marshal

hashtags = [{"id": 1, "name": u"Buy groceries"},
            {"id": 2, "name": u"Learn Python"}]


todo_parser = reqparse.RequestParser()
todo_parser.add_argument("hashtag", required=True)


hashtag_fields = {"name": fields.String, "uri": fields.Url("hashtag")}


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
        self.reqparse.add_argument("description", type=str, default="",
                                   location="json")
        super(HashtagListAPI, self).__init__()

    def get(self):
        return {"hashtags":
                [marshal(hashtag, hashtag_fields) for hashtag in hashtags]}

    def post(self):
        args = self.reqparse.parse_args()
        hashtag = {
            "id": hashtags[-1]["id"] + 1,
            "name": args["name"],
        }
        hashtags.append(hashtag)
        return {"hashtag": marshal(hashtag, hashtag_fields)}, 201


class HashtagAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, location="json")
        super(HashtagAPI, self).__init__()

    def get(self, id):
        hashtag = [hashtag for hashtag in hashtags if hashtag["id"] == id]
        if len(hashtag) == 0:
            abort(404)
        return {"hashtag": marshal(hashtags[0], hashtag_fields)}

    def put(self, id):
        hashtag = [hashtag for hashtag in hashtags if hashtag["id"] == id]
        if len(hashtag) == 0:
            abort(404)
        hashtag = hashtag[0]
        args = self.reqparse.parse_args()
        if "name" not in args.items():
            abort(400)
        for k, v in args.items():
            if v is not None:
                hashtag[k] = v
        return {"hashtag": marshal(hashtag, hashtag_fields)}

    def delete(self, id):
        hashtag = [hashtag for hashtag in hashtags if hashtag["id"] == id]
        if len(hashtag) == 0:
            abort(404)
        hashtags.remove(hashtag[0])
        return {"result": True}
