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
    if not activeUser:
        return jsonify(message = "Email is not registered"), 401
    if activeUser.role==True:
        return jsonify(message = "Your account is blocked, please contact Admin."), 403
    if activeUser.password != password:
        return jsonify(message = "Wrong password, Please try again."), 401
    authToken = create_access_token(identity = activeUser)
    return jsonify(authToken=authToken, role = activeUser.role, userId = activeUser.id, userName = activeUser.userName)

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
    HmsAppointments = Appointment.query.all()
    
    doctors = []
    
    for doctorUser in HmsDoctors:
        d = {}
        d["userId"]  = doctorUser.id
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

    activeDoctor = Doctor.query.get(id)

    if not activeDoctor:
        return jsonify(message="Doctor Not Found.. :("), 404

    activeUser = activeDoctor.user
    department = activeDoctor.department

    if request.method == "GET":

        resultPass = {
            "activeUser": {
                "id": activeUser.id,
                "userName": activeUser.userName,
                "email": activeUser.email
            },
            "doctor": {
                "doctor_id": activeDoctor.id,
                "doctorName": activeDoctor.doctorName,
                "specialization": activeDoctor.specialization,
                "availability": activeDoctor.availability
            },
            "department": {
                "departmentId": department.id,
                "departmentName": department.departmentName,
                "description": department.deptDescription
            }
        }

        return jsonify(resultPass)

    data = request.get_json()

    activeUser.email = data.get("email", activeUser.email)
    activeUser.userName = data.get("userName", activeUser.userName)

    if data.get("password"):
        activeUser.password = data.get("password")
    activeDoctor.doctorName = activeUser.userName
    activeDoctor.specialization = data.get("specialization", activeDoctor.specialization)
    activeDoctor.availability = data.get("availability", activeDoctor.availability)

    department.departmentName = data.get("departmentName", department.departmentName)
    department.deptDescription = data.get("description", department.deptDescription)

    db.session.commit()

    return jsonify(message="doctor updated"), 200
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
        return jsonify(message="Patient Not Found"), 404

    if request.method == "GET":
        return jsonify({
            "activeUser": {
                "id": activePatient.id,
                "userName": activePatient.userName,
                "email": activePatient.email
            }
        })

    data = request.get_json()

    activePatient.email = data.get("email", activePatient.email)
    activePatient.password = data.get("password", activePatient.password)
    activePatient.userName = data.get("userName", activePatient.userName)

    db.session.commit()

    return jsonify(message="Patient Data Updated.")

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

@app.route("/hms/adminFullTreatmentHistory:<int:patientId>", methods=["GET"])
@role_required("admin")
def adminFullTreatmentHistory(patientId):

    patient = Patient.query.get(patientId)

    if not patient:
        return jsonify(message="Patient not found"), 404

    treatments_q = Treatment.query.filter_by(
        patientId=patient.id
    ).all()

    result = []

    for t in treatments_q:

        doctor = Doctor.query.get(t.doctorId)
        appointment = Appointment.query.get(t.appointmentId)

        entry = {
            "treatment_id": t.id,
            "diagnosis": t.diagnosis,
            "prescription": t.prescription,
            "notes": t.notes,
            "medicines": t.medicines,
            "testsDone": t.testsDone,
            "visitType": t.visiteType,
            "doctor": {
                "doctor_id": doctor.id if doctor else None,
                "doctor_name": doctor.doctorName if doctor else None
            },
            "appointment": {
                "appointment_id": appointment.id if appointment else None,
                "date": appointment.date.isoformat() if appointment and appointment.date else None,
                "time": appointment.time.isoformat() if appointment and appointment.time else None,
                "status": appointment.status if appointment else None
            }
        }

        result.append(entry)

    return jsonify({
        "patient": {
            "patient_id": patient.id,
            "patient_name": patient.patientName
        },
        "treatments": result
    }), 200

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

@app.route("/hms/doctorDashboard:<int:id>")
@jwt_required("doctor")
def doctorDashboard(id):
    activeDoctor = User.query.filter_by(id=id, role="doctor").first()
    
    if not activeDoctor:
        return jsonify(message="Doctor Not Found"), 404

    doctor = activeDoctor.doctorProfile

    upcommintAppointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == "Booked"
    ).all()

    completedAppointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == "completed"
    ).all()

    comming = []

    for appointment in upcommintAppointments:
        appointments = {}
        appointments["id"] = appointment.id

        appointments["date"] = appointment.date.isoformat() if appointment.date else None
        appointments["time"] = appointment.time.isoformat() if appointment.time else None

        if appointment.patient:
            appointments["patientId"] = appointment.patient.id
            appointments["patientName"] = appointment.patient.patientName

        comming.append(appointments)

    completed = []

    for complete in completedAppointments:
        completeResult = {}
        completeResult["id"] = complete.id

        completeResult["date"] = complete.date.isoformat() if complete.date else None
        completeResult["time"] = complete.time.isoformat() if complete.time else None

        if complete.patient:
            completeResult["patientId"] = complete.patient.id
            completeResult["patientName"] = complete.patient.patientName

        completed.append(completeResult)

    out = {
        "this_doctor": {
            "user_id": activeDoctor.id,
            "username": activeDoctor.userName
        },
        "doctor": {
            "doctor_id": doctor.id,
            "doctor_name": doctor.doctorName,
            "availability": doctor.availability
        },
        "upcomming_appointments": comming,
        "completed_appointments": completed
    }

    return jsonify(out), 200

@app.route("/hms/updatePatient:<int:appointmentId>:<int:userId>", methods=["GET", "POST"])
@role_required("doctor")
def updatePatient(appointmentId, userId):

    this_doctor_user = User.query.filter_by(id=userId, role="doctor").first()
    if not this_doctor_user:
        return jsonify(message="Doctor not found"), 404

    doctor = this_doctor_user.doctorProfile

    appointment = Appointment.query.get(appointmentId)
    if not appointment:
        return jsonify(message="Appointment not found"), 404

    patient = appointment.patient

    treatments_q = Treatment.query.filter_by(
        doctorId=doctor.id,
        patientId=patient.id
    ).all()

    if request.method == "GET":

        treatments = []
        for t in treatments_q:
            treatments.append({
                "diagnosis": t.diagnosis,
                "prescription": t.prescription,
                "notes": t.notes,
                "appointmentId": t.appointmentId
            })

        out = {
            "patient": {
                "patient_id": patient.id,
                "patient_name": patient.patientName
            },
            "this_doctor": {
                "user_id": this_doctor_user.id,
                "username": this_doctor_user.userName
            },
            "appointment": {
                "appointment_id": appointment.id,
                "date": appointment.date.isoformat() if appointment.date else None,
                "time": appointment.time.isoformat() if appointment.time else None
            },
            "doctor": {
                "doctor_id": doctor.id,
                "doctor_name": doctor.doctorName
            },
            "treatments": treatments
        }

        return jsonify(out)

    visit_type = request.json.get("visit_type")
    medicines = request.json.get("medicines")
    tests_done = request.json.get("tests_done")
    diagnosis = request.json.get("diagnosis")
    prescription = request.json.get("prescription")
    notes = request.json.get("notes")

    treatment = Treatment(
        diagnosis=diagnosis,
        prescription=prescription,
        notes=notes,
        appointmentId=appointment.id,
        doctorId=doctor.id,
        patientId=patient.id,
        visiteType=visit_type,
        medicines=medicines,
        testsDone=tests_done
    )

    db.session.add(treatment)
    db.session.commit()

    return jsonify(message="Treatment saved"), 200

@app.route("/hms/completeTreatment:<int:id>")
@role_required("doctor")
def completeTreatment(id):
    appointments = Appointment.query.get(id)
    appointments.status = "completed"
    db.session.commit()
    return jsonify(message= "Treatment completed")

@app.route("/hms/deleteRequest:<int:id>")
@role_required("doctor")
def doctorDeleteRequest(id):
    appointment = Appointment.query.get(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify(message="Request Deleted")

@app.route("/hms/viewPatientTreatments:<int:patientId>:<int:userId>", methods=["GET"])
@role_required("doctor")
def viewPatientTreatments(patientId, userId):

    doctor_user = User.query.filter_by(id=userId, role="doctor").first()
    doctor = doctor_user.doctorProfile
    patient = Patient.query.get(patientId)
    treatments = Treatment.query.filter_by(
        doctorId=doctor.id,
        patientId=patient.id
    ).all()

    result = []

    for t in treatments:
        result.append({
            "diagnosis": t.diagnosis,
            "prescription": t.prescription,
            "notes": t.notes,
            "medicines": t.medicines,
            "testsDone": t.testsDone,
            "visitType": t.visiteType,
            "appointmentId": t.appointmentId
        })

    return jsonify({
        "patient": {
            "id": patient.id,
            "name": patient.patientName
        },
        "treatments": result
    }), 200

@app.route("/hms/setAvailability:<int:userId>", methods=["GET", "POST"])
@role_required("doctor")
def setAvailability(userId):

    this_doctor_user = User.query.filter_by(id=userId, role="doctor").first()
    if not this_doctor_user:
        return jsonify(message="Doctor not found"), 404

    doctorProfile = this_doctor_user.doctorProfile

    today = date.today()
    min_date = today.isoformat()
    max_date = (today + timedelta(days=7)).isoformat()

    message = None

    if request.method == "POST":
        selected_date = request.json.get("date")
        morning_slot = bool(request.json.get("morningSlot"))
        evening_slot = bool(request.json.get("eveningSlot"))

        selected_date_obj = date.fromisoformat(selected_date)

        existing = Doctor.query.filter_by(
            userId=this_doctor_user.id,
            date=selected_date_obj
        ).first()

        if existing:
            existing.morningSlot = morning_slot
            existing.eveningSlot = evening_slot
        else:
            new_availability = Doctor(
                doctorName=doctorProfile.doctorName,
                specialization=doctorProfile.specialization,
                availability="available",
                date=selected_date_obj,
                morningSlot=morning_slot,
                eveningSlot=evening_slot,
                userId=this_doctor_user.id,
                departmentId=doctorProfile.departmentId
            )
            db.session.add(new_availability)

        db.session.commit()
        message = "Availability set successfully."

    availabilities_q = Doctor.query.filter(
        Doctor.userId == this_doctor_user.id
    ).all()

    availabilities = []

    for a in availabilities_q:
        availabilities.append({
            "date": a.date.isoformat() if a.date else None,
            "morningSlot": a.morningSlot,
            "eveningSlot": a.eveningSlot
        })

    return jsonify({
        "min_date": min_date,
        "max_date": max_date,
        "availabilities": availabilities,
        "this_doctor": {
            "user_id": this_doctor_user.id,
            "username": this_doctor_user.userName
        },
        "message": message
    })