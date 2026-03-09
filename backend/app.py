from flask import Flask
from apk.models import *
from apk.security import *
from apk.config import *
from flask_cors import *
from apk.create_db import db
from datetime import timedelta
from apk.celery_init import celery_init_app
from flask_mail import Mail   
from apk.cache import cache

app = None
mail = Mail()   

def app_building():
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(LocalDevelopmentConfig)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=4)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app) 
    cache.init_app(app)

    CORS(app, supports_credentials=True)
    app.app_context().push()
    return app


app = app_building()

celery = celery_init_app(app)

from apk.controllers import *

if __name__=="__main__":
    # db.create_all()
    # this_new_user = User(userName="admin01", email="admin@gmail.com", password="12", role="admin", isBlock=False)
    # db.session.add(this_new_user)
    # db.session.commit()
    # print("Dear Developer Apka Database ready hai yoohooo:) !!")
    app.run()