from flask import Flask
from flask_restful import Resource, Api, reqparse
from .subtitle import searchForTitles
from .subtitle import retrieveTitleSubtitles
from .subtitle import downloadSubtitle

app = Flask(__name__)

api = Api(app)

class Titles(Resource):
    def get(self, searchString):
        return searchForTitles(searchString), 200

class Subtitles(Resource):
    def get(self, titleId):
        return retrieveTitleSubtitles(titleId), 200

class Download(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('subtitleId', required=True)
        parser.add_argument('outputName', required=True)

        args = parser.parse_args()
        return downloadSubtitle(args['subtitleId'], args['outputName']), 201
        

api.add_resource(Titles, '/titles/<string:searchString>')
api.add_resource(Subtitles, '/subtitles/<string:titleId>')
api.add_resource(Download, '/download')

