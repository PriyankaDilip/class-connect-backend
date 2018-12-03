#archive containing Google login backend version

#from __future__ import print_function
from flask import Flask, request, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

import json
from db_security import db, User
from config_security import config
#import datetime
#from googleapiclient.discovery import build
#from httplib2 import Http
#from oauth2client import file, client, tools
import users_dao

#SCOPES = 'https://www.googleapis.com/auth/calendar'
#GMT_OFF = '-04:00' #EST

db_filename = "ohinfo.db"
app = Flask(__name__)

#new since implementing ORM
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config.from_object(config['dev'])
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

""" IS THIS NEEDED HERE"""
db.init_app(app)
with app.app_context():
    db.create_all()

#def extract_token(request):

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

"""OAuth Session Creation"""

def get_google_auth(state=None, token=None):
    #no params provided -> create new OAuth2Session with new state
    if token:
        oauth = OAuth2Session(
            Auth.CLIENT_ID, 
            token=token)
    #state provided
    if state: 
        oauth = OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri = Auth.REDIRECT_URI)
    #token provided i.e. final step thus only need access_token
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri = Auth.REDIRECT_URI,
        scope=Auth.SCOPE)

    return oauth


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url( Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state #store value of state in cookie for later use
    return render_template('login.html', auth_url=auth_url)

@app.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    #if code and state params not in URL, user tried to access directly  therefore redirect user
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            #Create own OAuthSession2 obj -> pass state param, then try to get access_token from Google
            token = google.fetch_token( Auth.TOKEN_URI, client_secret=Auth.CLIENT_SECRET, authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        #if access_token received, again create new OAuth2Session by setting token param
        #THEN access user's info
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = get_user_by_email(email)
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# #@app.route('/register/', methods=['POST'])
# #def register_account():

#------------"Security routes above, app routes below"--------------------------


#@app.route('/register/', methods=['POST'])
#def register_account():


""" @app.route('/session/', methods=['POST'])
def update_session():
    success, update_token = extract_token(request)

    if not success:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except: 
        return json.dumps({'error': 'Invalid update token.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    }) """

""" @app.route('/secret/', methods=['GET'])
def secret_message():
    success, session_token = extract_token(request)

    if not success:
        return session_token 

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({'error': 'Invalid session token.'})

    return json.dumps({'message': 'You have successfully implemented sessions.'}) """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
