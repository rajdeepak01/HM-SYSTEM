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

@app.route("/hms/login", methods= ["GET", "POST"])
def hmsLogin():
    email = request.json.get("email")
    password = request.json.get("password")
    activeUser = User.query.filter_by(email=email).first()
    print(email)
    print(password)
    print(activeUser.role)
    if not activeUser:
        return jsonify(message = "Email is not registered"), 401
    if activeUser.role==True:
        return jsonify(message = "Your account is blocked, please contact Admin."), 403
    if activeUser.password != password:
        return jsonify(message = "Wrong password, Please try again."), 401
    authToken = create_access_token(identity = activeUser)
    return jsonify(authToken=authToken, role = activeUser.role, user_id = activeUser.id, userName = activeUser.userName)

@app.route("/hms/register", methods = ["GET", "POST"])
def hmsUserRegister():
    userName = request.json.get("userName")
    email    = request.json.get("email")
    password = request.json.get("password")
    activeUser = User.query.filter_by(email=email).first()
    if activeUser:
        return jsonify(message = "User Already exist")
    addUser = User(userName = userName, email = email, password= password)
    db.session.add(addUser)
    db.session.commit()
    return jsonify(message="Registration Successfull..! Please Login")

@app.route("/hms/adminDashboard", methods = ["GET"])
def HmsAdminDashboard():
    message = request.args.get("message")
    err = request.args.get("err")
    HmsDoctors = User.query.filter_by(role = "doctor").all()
    HmsPatients = User.query.filter_by(role = "patient").all()
    HmsAppointments = Appointment.query.filter_by(status = "Booked").all()
    
    doctors = []
    
    for doctorUser in HmsDoctors:
        d = {}
        d["user_id"]  = doctorUser.id
        d["userName"] = doctorUser.userName
        d["email"]    = doctorUser.email
        d["isBlock"] = getattr(doctorUser, "isBlock", False)
        doctorProfile = getattr(doctorUser, "doctorProfile", None)

        if doctorProfile:
            d["doctorId"]  = doctorProfile.id
            d["doctorName"] = doctorProfile.doctorName
            d["specialization"] = doctorProfile.specialization
            d["availability"] = doctorProfile.availability
            department = getattr(doctorProfile, "department", None)

            if department:
                d["departmentId"] = department.id
                d["departmentName"] = department.departmentName
            doctors.append(d)
    
    patients = []

    for patientUser in HmsPatients:
        p = {}
        p["userId"] = patientUser.id
        p["userName"] = patientUser.userName
        p["email"] = patientUser.email
        p["isBlock"] = getattr(patientUser, "isBlock", False)
        patientProfile = getattr(patientUser, "patientProfile", None)

        if patientProfile:
            p["patientId"] = patientProfile.id
            p["patientName"] = patientProfile.patientName
        patients.append(p)
        
    appointments = []
    
    for appointment in HmsAppointments:
        a = {}
        a["appointment_id"] = appointment.id
        a["date"] = appointment.date.isoformat() if getattr(appointment, "date", None) else None
        a["time"] = appointment.time.isoformat() if getattr(appointment, "time", None) else None
        a["status"] = appointment.status
        if getattr(appointment, "patient", None):
            a["patientId"] = appointment.patient.id
            a["patientName"] = appointment.patient.patientName
        if getattr(appointment, "doctor", None):
            a["doctorId"] = appointment.doctor.id
            a["doctorName"] = appointment.doctor.doctorName
            if getattr(appointment.doctor, "department", None):
                a["departmentName"] = appointment.doctor.department.departmentName
        appointments.append(a)
    return jsonify(doctors=doctors, patients=patients, appointments=appointments, message=message, err=err)

