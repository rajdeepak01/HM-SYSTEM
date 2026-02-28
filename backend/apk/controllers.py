from flask import current_app as app, request, jsonify, abort
from .models import *
from .create_db import db
from flask_jwt_extended import create_access_token, jwt_required, current_user
from functools import wraps
from datetime import date, timedelta, datetime
from sqlalchemy import or_

def role_required(required_type):
    def wrapper(fn):
        @wraps(fn)
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
@role_required("admin")
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

@app.route("/hms/addDoctor", methods=["GET", "POST"])
@role_required("admin")
def addDoctor():
    doctorName = request.json.get("doctorName")
    email = request.json.get("email")
    password = request.json.get("password")
    specialization = request.json.get("specialization")
    availability = request.json.get("availability")
    departmentName = request.json.get("departmentName")
    deptDescription = request.json.get("deptDescription")

    if User.query.filter_by(email=email).first():
        return jsonify(message="Doctor already exists")

    newUser = User(
        userName=doctorName,
        email=email,
        password=password,
        role="doctor"
    )
    db.session.add(newUser)
    db.session.commit()

    activeDepartment = Department.query.filter_by(departmentName=departmentName).first()
    if not activeDepartment:
        activeDepartment = Department(
            departmentName=departmentName,
            deptDescription=deptDescription
        )
        db.session.add(activeDepartment)
        db.session.commit()

    newDoctor = Doctor(
        doctorName=doctorName,
        specialization=specialization,
        availability=availability,
        userId=newUser.id,
        departmentId=activeDepartment.id
    )
    db.session.add(newDoctor)
    db.session.commit()

    return jsonify(message="Doctor added successfully")

@app.route("/hms/editDoctor:<int:id>", methods=["GET", "POST"])
@role_required("admin")
def editDoctor(id):
    activeUser = User.query.get(id)
    if not activeUser:
        return jsonify(message = "Doctor Not Found.. :(")
    if request.method == "GET":
        activeDoctor = activeUser.doctorProfile
        department = getattr(activeDoctor, "department")
        resultPass = {}
        resultPass["activeUser"] = {"id": activeUser.id,
                                    "userName": activeUser.userName,
                                     "email" : activeUser.email }
        if activeDoctor:
            resultPass["doctor"] = {"doctor_id":activeDoctor.id,
                             "doctorName": activeDoctor.doctorName,
                             "specialization": department.specialization,
                             "description": department.deptDescription}
        if department:
            resultPass["department"] = {"departmentId": department.id,
                                        "departmentName": department.departmentName,
                                        "description": department.deptDescription}
        return resultPass
    
    activeUser.email = request.json.get("email", activeUser.email)
    activeUser.password = request.json.get("password", activeUser.password)
    activeUser.userName = request.json.get("userName", activeUser.userName)
    activeDoctor = activeUser.doctorProfile
    activeDoctor.specialization = request.json.get("specialization", activeDoctor.specialization)
    department = activeDoctor.department
    activeDoctor.availability = request.json.get("availability", activeDoctor.availability)
    department.departmentName = request.json.get("departmentName", department.departmentName)
    department.deptDescription = request.json.get("description", department.deptDescription)
    db.session.commit()
    return jsonify(message= "doctor updated")

@app.route("/hms/deleteDoctor:<int:id>", methods=["Delete"])
@role_required("admin")
def deleteDoctor(id):
    activeDoctor = User.query.get(id)
    if activeDoctor:
        db.session.delete(activeDoctor)
        db.session.commit()
        return jsonify(message= "Doctor Delete :(")
    else:
        return jsonify(message= "Doctor Not Found :(")
    
@app.route("/hms/blockDoctor:<int:id>", methods=['POST'])
@role_required("admin")
def blockDoctor(id):
    activeDoctor = User.query.get(id)
    if not activeDoctor:
        return jsonify(message = "Doctor Not Found")
    else:
        activeDoctor.isBlock = "1"
        db.session.commit()
        return jsonify(message = f"{activeDoctor.userName} has been blocked")

@app.route("/hms/unblockDoctor:<int:id>", methods=['POST'])
@role_required("admin")
def unblockDoctor(id):
    activeDoctor = User.query.get(id)
    if not activeDoctor:
        return jsonify(message = "Doctor Not Found")
    else:
        activeDoctor.isBlock = "0"
        db.session.commit()
        return jsonify(message = f"{activeDoctor.userName} has been unblocked")

@app.route("/hms/editPatient:<int:id>", methods=["GET", "POST"])
@role_required("admin")
def editPatient(id):
    activePatient = User.query.get(id)
    if not activePatient:
        return jsonify(message = "Patient Not Found")
    else:
        activePatient.email = request.json.get("email", activePatient.email)
        activePatient.password = request.json.get("password", activePatient.password)
        activePatient.userName = request.json.get("userName", activePatient.userName)
        db.session.commit()
        return jsonify(message = "Patient Data Updated.")
    
@app.route("/hms/blockPatient:<int:id>", methods=['POST'])
@role_required("admin")
def blockPatient(id):
    activePatient = User.query.get(id)
    if not activePatient:
        return jsonify(message = "Patient Not Found")
    else:
        activePatient.isBlock = "1"
        db.session.commit()
        return jsonify(message = f"{activePatient.userName} has been blocked")

@app.route("/hms/unblockPatient:<int:id>", methods=['POST'])
@role_required("admin")
def unblockPatient(id):
    activePatient = User.query.get(id)
    if not activePatient:
        return jsonify(message = "Patient Not Found")
    else:
        activePatient.isBlock = "0"
        db.session.commit()
        return jsonify(message = f"{activePatient.userName} has been unblocked")
    
@app.route("/hms/deletePatient:<int:id>", methods = ["Delete"])
def deletePatient(id):
    activePatient = User.query.get(id)
    if not activePatient:
        return jsonify(message = "Patient Not Found")
    else:
        db.session.delete(activePatient)
        db.session.commit()
        return jsonify(message = "Patient has been deleted :( ")

@app.route("/hms/adminSearch")
@role_required("admin")
def adminSearch():

    keyword = request.args.get("search", "")
    pattern = f"%{keyword}%"

    users = (
        db.session.query(User)
        .filter(
            or_(
                User.userName.ilike(pattern),
                User.email.ilike(pattern),
                User.role.ilike(pattern)
            )
        )
        .all()
    )

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "userName": user.userName,
            "email": user.email,
            "role": user.role,
            "isBlock": user.isBlock
        })

    return jsonify(activeUsers=result)
