from apk.create_db import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String, unique=True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String, default = "patient")
    isBlock = db.Column(db.String, default=False)
    doctorProfile = db.relationship('Doctor', backref="user", uselist = False, cascade = "all, delete-orphan")
    patientProfile = db.relationship("Patient", backref="user", uselist= False, cascade = "all, delete-orphan")

class Department(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    departmentName = db.Column(db.String)
    deptDescription = db.Column(db.String)
    doctors = db.relationship("Doctor", backref= "department", cascade = "all, delete", lazy = True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    doctorName = db.Column(db.String(), nullable = False)
    specialization = db.Column(db.String, nullable = False)
    date = db.Column(db.Date)
    availability = db.Column(db.String, nullable = False)
    morningSlot = db.Column(db.Boolean, default=False)
    eveningSlot = db.Column(db.Boolean, default = False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id", ondelete= "CASCADE"), nullable=False)
    departmentId = db.Column(db.Integer, db.ForeignKey("department.id", ondelete="SET NULL"), nullable= False)
    appointments = db.relationship("Appointment", backref="doctor", cascade = "all, delete-orphan", lazy=True)
    treatments = db.relationship("Treatment", backref ="doctor", cascade = "all, delete-orphan", lazy = True)
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    patientName = db.Column(db.String, nullable= False)
    age = db.Column(db.Integer, nullable= False)
    gender = db.Column(db.String, nullable = False)
    contact = db.Column(db.String, nullable = False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable = False)
    appointments = db.relationship("Appointment", backref="patient", cascade="all, delete-orphan", lazy = True)
    treatment = db.relationship("Treatment", backref= "patient", cascade = "all, delete-orphan", lazy= True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable= False)
    time = db.Column(db.Time, nullable = False)
    status= db.Column(db.String, default = "Booked")
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id", ondelete= "CASCADE"), nullable= False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id", ondelete="CASCADE"), nullable =False)
    treatment = db.relationship("Treatment", backref ="appointment", cascade = "all, delete-orphan", uselist= False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    diagnosis = db.Column(db.String, nullable =True)
    prescription = db.Column(db.String, nullable = True)
    notes = db.Column(db.String, nullable=False)
    medicines = db.Column(db.String, nullable = False)
    testsDone = db.Column(db.String, nullable=False)
    visiteType = db.Column(db.String, default = "NA")
    appointmentId = db.Column(db.Integer, db.ForeignKey("appointment.id", ondelete="CASCADE"), nullable = False)
    doctorId = db.Column(db.Integer, db.ForeignKey("doctor.id", ondelete="CASCADE"), nullable=False)
    patientId = db.Column(db.Integer, db.ForeignKey("patient.id", ondelete="CASCADE"), nullable=False)