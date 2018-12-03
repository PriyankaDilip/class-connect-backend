# has our Google OAuth credentials and our app configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    CLIENT_ID = ('688061596571-3cl3n0uho6qe34hjqj2apincmqk86ddj' '.apps.googleusercontent.com')
    CLIENT_SECRET = 'JXf71c_jfCam1S71BJalDyPZ'
    REDIRECT_URI = 'https://localost:5000/gCallback' #set in Google Dev Console
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth' #where user is taken
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token' #used to exchange temp token for an access_token
    USER_INFO = 'https://www.googleapis.come/userinfo/v2/me' #retrieve user info after successful auth

class Config:
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"

class DevConfig(Config):
    DEBUG = TrueSQLACLHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")

class ProdConfig(Config):
    DEBUG = TrueSQLACLHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")

config = {
    "dev" : DevConfig,
    "prod" : ProdConfig,
    "default" : DevConfig
}