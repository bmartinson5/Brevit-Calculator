"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""



import os
import flask
import pdb
from flask import request
from flask import g
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
from bson.json_util import loads
import logging
import json

from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)


###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
app.port = CONFIG.PORT
print("PORT!!= ", app.port)
MONGO_URL = "mongodb://test:pass123@ds157740.mlab.com:57740/proj5db"
client = MongoClient(MONGO_URL)
db = client.get_database("proj5db")
collection = db.records
users = db.users

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')
    

@app.route("/api/register", methods=["Post"])
def register():
    user = request.form.get("username")
    pass = request.form.get("password")
    if user == None or pass == None:
	return flask.jsonify({"result": "Invalid input}), 400
    if users.find_one({"username": user}) == "None":
	#userName is unique
        hash = hash_password(pass)
        users.insert({"username": user, "password":pass})
        return flask.jsonify({"result": "user registered"}), 201
    else:
        return flask.jsonify({"result": "username not unique"}), 400
    

    

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.route("/_display_data")
def _display_data():
    return flask.render_template('display.html')

@app.route("/_get_port")
def _get_port():
    result = { "port": app.port }
    return flask.jsonify(result=result)

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############



@app.route("/_display_info")
def _display_info():
    allEntries = collection.find()
    count = 1
    result = {}
    for entry in allEntries:
        entry.pop('_id')
        result[ count ] = entry
        count = count + 1
    return flask.jsonify(result = result)


def add_entry(start, distance, km, open, close):
    currentEntries = flask.session['entries']
    if currentEntries == None:
        currentEntries = []

    newEntry = { 'start': start, 'distance': distance, 'km': km, 'openTime':open, 'closeTime':close }
    currentEntries.append(newEntry)
    print(currentEntries)
    flask.session['entries'] = currentEntries 


@app.route("/_insert_data")
def _insert_data():
    for entry in flask.session['entries']:
        print(entry)
        collection.insert(entry)
    return 'ok'




@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    miles = request.args.get('miles', 999, type=float)
    date = request.args.get('beginDate', type=str)
    time = request.args.get('beginTime', type=str)
    distance = request.args.get('distance', type=str)
    startTime = arrow.get(date + ' ' + time, 'YYYY-MM-DD HH:mm')
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    print('start= ', startTime)
    open_time = acp_times.open_time(km, distance, startTime)
    close_time = acp_times.close_time(km, distance, startTime)



    if open_time != '-1':
        open_time = open_time.isoformat()
        close_time = close_time.isoformat()
        startTime = startTime.isoformat()
        result = {"open": open_time, "close": close_time, "kilos": km}
        add_entry(startTime, distance, km, open_time, close_time)
    else:
        result = {"open": -1, "kilos": km}


    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
