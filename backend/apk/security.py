from flask_jwt_extended import JWTManager
from apk.models import *

jwt = JWTManager()

@jwt.user_identity_loader
def load(user):
    return user.userName

@jwt.user_lookup_loader
def user_lookup_callback(__jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(userName = identity)
