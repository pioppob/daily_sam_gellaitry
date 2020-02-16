
import os

class Config:

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-duper-secret'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TRACKLIST_DIR = os.listdir(BASEDIR + '/static/tracks')
    MAX_WORKERS = 70

    JSON_TRACK_DATA = os.path.join(BASEDIR, 'sc.json')
    CLIENT_ID = 'qeWb21nmKO1VUDsY88W1341i7kO1JXeK' # Authorization required by soundcloud API