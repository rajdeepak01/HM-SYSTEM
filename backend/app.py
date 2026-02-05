from flask import Flask
from apk.models import *
from apk.security import *
from apk.config import *
from flask_cors import *
from apk.create_db import db

app = None

def app_building():
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)
    app.app_context().push()
    return app

app = app_building()

from apk.controllers import *

if __name__=="__main__":
    # db.create_all()
    # this_new_user = User(username="admin01", email="admin@hsm.com", password="hms1234", role="admin")
    # db.session.add(this_new_user)
    # print("Dear Developer Apka Database ready hai yoohooo:) !!")
    app.run()
    