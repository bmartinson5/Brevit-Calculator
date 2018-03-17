
from flask import Flask, request
import flask
from flask_restful import Resource, Api
from pymongo import MongoClient

MONGO_URL = "mongodb://test:pass123@ds157740.mlab.com:57740/proj5db"
client = MongoClient(MONGO_URL)
db = client.get_database("proj5db")
collection = db.records

# Instantiate the app
app = Flask(__name__)
api = Api(app)

class AllTimes(Resource):
    
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = {}
        for entry in allEntries:
            if top != None and count > int(top):
                break
            entry.pop('_id')
            result[ count ] = entry
            count = count + 1
        return flask.jsonify(result = result)

class OpenTimes(Resource):
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = {}
        for entry in allEntries:
            if top != None and count > int(top):
                break
            entry.pop('_id')
            entry.pop('Close')
            result[ count ] = entry
            count = count + 1
        return flask.jsonify(result = result)

class CloseTimes(Resource):
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = {}
        for entry in allEntries:
            if top != None and count > int(top):
                break
            entry.pop('_id')
            entry.pop('Open')
            result[ count ] = entry
            print(entry)
            count = count + 1
        return flask.jsonify(result = result)


class AllCSV(Resource):
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = ""
        for entry in allEntries:
            if top != None and count > int(top):
                break
            if count == 1:
                result = "Open Times: " + entry['Open']
            else:
                result = result + ", " + entry['Open']
            count += 1

        count = 1
        result2 = ""
        allEntries = collection.find()
        for entry in allEntries:
            if top != None and count > int(top):
                break
            if count == 1:
                result2 = result2 + "Close Times: " + entry['Close']
            else:
                result2 = result2 + ", " + entry['Close']
            count += 1


        return [result, result2]

class CloseCSV(Resource):
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = ""
        for entry in allEntries:
            if top != None and count > int(top):
                break
            if count == 1:
                result = "Close Times: " + entry['Close']
            else:
                result = result + ", " + entry['Close']
            count += 1
        return result

class OpenCSV(Resource):
    def get(self):

        top = request.args.get('top')
        allEntries = collection.find()
        count = 1
        result = ""
        for entry in allEntries:
            if top != None and count > int(top):
                break
            if count == 1:
                result = "Open Times: " + entry['Open']
            else:
                result = result + ", " + entry['Open']
            count += 1
        return result

# Create routes
# Another way, without decorators
api.add_resource(AllTimes, '/listAll', '/listAll/json')
api.add_resource(OpenTimes, '/listOpenOnly/', '/listOpenOnly/json')
api.add_resource(CloseTimes, '/listCloseOnly', '/listCloseOnly/json')
api.add_resource(OpenCSV, '/listOpenOnly/csv') 
api.add_resource(CloseCSV, '/listCloseOnly/csv')
api.add_resource(AllCSV, '/listAll/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
