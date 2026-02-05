from flask import current_app as app, request, jsonify, abort
from .models import *
from .create_db import db
from flask_jwt_extended import create_access_token, jwt_required, current_user
from functools import wraps
from datetime import date, timedelta, datetime

def role_required(required_type):
    def wrapper(fn):
        @wrapper(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if getattr(current_user, "role", None) != required_type:
                return jsonify(message="sorry but youre Not authorized to access!!"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route("/", methods = ["GET"])
def SystemStart():
    return jsonify(message="Welcome to HM-System")
