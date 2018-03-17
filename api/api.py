
from flask import Flask, request, abort, jsonify, url_for
import flask
from flask_restful import Resource, Api
from pymongo import MongoClient
from base64 import b64decode
import pdb
import config
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import flask_login
from flask_login import login_user, current_user
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from urllib.parse import urlparse, urljoin


MONGO_URL = "mongodb://test:pass123@ds157740.mlab.com:57740/proj5db"
client = MongoClient(MONGO_URL)
db = client.get_database("proj5db")
collection = db.records
users = db.users
counter = db.counter
CONFIG = config.configuration()
Key = CONFIG.SECRET_KEY


# Instantiate the app
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = ('/api/login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password') 
    rememberMe = BooleanField('remember')

def safe_url(url):
    urlRef = urlparse(request.host_url)
    test = urlparse(urljoin(request.host_url, url))
    return test.scheme in ('http', 'https') and urlRef.netloc == test.netloc

@login_manager.user_loader
def load_user(userId):
    if not users.find({"_id": userId}):
        return None
    return User(userId)


@app.route('/api/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = request.form.get('username')
        password = request.form.get('password')
        rememberMe = request.form.get('remember')
        
        hashval = hash_password(password)
        if verify_password(user, hashval):
            document = users.find_one({"username": user})
            userId = document['_id']
            user = User(userId)
            login_user(user, remember=rememberMe)
            flask.flash("You have successfully Logged into API")

            next = flask.request.args.get('next')
            if not safe_url(next):
                return flask.abort(400)
 
        return flask.redirect(next or flask.url_for('getToken'))
    return flask.render_template('login.html', form=form)
    

@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    flask.flash("Logout successful")
    return flask.render_template('logout.html')




def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

def generate_auth_token(expiration=600):
    s = Serializer(Key, expires_in=expiration)
    return s.dumps({'id': 1})

def verify_auth_token(token):
    s = Serializer(Key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except SignatureExpired:
        return None
    return "Success"

    

@auth.verify_password
def verifyUser(token, password):
    if verify_auth_token(token) == None:
        return False
    return True
    

@app.route("/api/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = request.form.get("username")
        password = request.form.get("password")
        if user == None or password == None:
            abort(400, 'Invalid Formatting of username or password')
        if users.find_one({"username": user}) == None:
	    #userName is unique
            hash = hash_password(password)

            #retrieve counter to set unique id of user in database
            countDocument = counter.find_one()
            count = countDocument['count']
            users.insert({"username": user, "password":hash, "_id":getNextIdCount(counter, 'id count')})
            id = countDocument['count']
            return flask.redirect(flask.url_for('getToken'))
        else:
            abort(400, 'Username already taken, must be unique')

    return flask.render_template('register.html', form=form)

def getNextIdCount(collection, name):
    return collection.find_and_modify(query= { '_id': name }, update={'$inc':{'count': 1}}, new=True).get('count')
    
    
@app.route("/api/token")
#@flask_login.login_required
def getToken():
    form = LoginForm()
    if not current_user.is_authenticated:
        return flask.render_template('login.html', form=form)
    token = generate_auth_token(600)
    return flask.jsonify({'token': token.decode(), 'duration': 600})

class User(flask_login.UserMixin):
    def __init__(self, id):
        self.id = id


class AllTimes(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        result = {}
        count = 1
        result = processJSON(result, top,  'openTime', 'closeTime')
        return flask.jsonify(result = result)

class OpenTimes(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        result = {}
        result = processJSON(result, top,  'openTime', None)
        return flask.jsonify(result = result)

class CloseTimes(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        result = {}
        result = processJSON(result, top,  'closeTime', None)
        return flask.jsonify(result = result)

class AllCSV(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        return processCSV(top, 'openTime', 'closeTime')


class CloseCSV(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        return processCSV(top, 'closeTime', None)


class OpenCSV(Resource):
    @auth.login_required
    def get(self):
        top = request.args.get('top')
        return processCSV(top, 'openTime', None)


def processCSV(top, timeType, timeType2):
        result = ""
        allEntries = collection.find()
        count = 1
        for entry in allEntries:
            if top != None and count > int(top):
                break
            elif count == 1:
                result = result + entry[timeType]
            else:
                result = result + ", " + entry[timeType]
            count += 1
            if timeType2 != None:
                if top != None and count > int(top):
                    break
                result = result + ", " + entry[timeType2]
                count = count + 1

        return result
    
def processJSON(result, top, timeType, timeType2):
        allEntries = collection.find()
        count = 1
        for entry in allEntries:
            if top != None and count > int(top):
                break
            result[ count ] = entry[timeType]
            count = count + 1
            if timeType2 != None:
                if top != None and count > int(top):
                    break
                result[ count ] = entry[timeType2]
                count = count + 1
        return result

# Create routes
# Another way, without decorators
api.add_resource(AllTimes, '/listAll', '/listAll/json')
api.add_resource(OpenTimes, '/listOpenOnly', '/listOpenOnly/json')
api.add_resource(CloseTimes, '/listCloseOnly', '/listCloseOnly/json')
api.add_resource(OpenCSV, '/listOpenOnly/csv') 
api.add_resource(CloseCSV, '/listCloseOnly/csv')
api.add_resource(AllCSV, '/listAll/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
