from datetime import date, time
from app import app
from apk.create_db import db
from apk.models import User, Department, Doctor, Patient, Appointment, Treatment


def init_db():
    with app.app_context():

        db.drop_all()
        db.create_all()

        users = []

        admin = User(
            userName="admin",
            email="admin@gmail.com",
            password="12",
            role="admin",
            isBlock=False
        )
        users.append(admin)

        for i in range(1, 6):
            users.append(
                User(
                    userName=f"doctor{i}",
                    email=f"doctor{i}@gmail.com",
                    password="12",
                    role="doctor",
                    isBlock=False
                )
            )

        for i in range(1, 6):
            users.append(
                User(
                    userName=f"patient{i}",
                    email=f"patient{i}@gmail.com",
                    password="12",
                    role="patient",
                    isBlock=False
                )
            )

        db.session.add_all(users)
        db.session.commit()

        
        departments = [
            Department(departmentName="Cardiology", deptDescription="Heart treatments"),
            Department(departmentName="Neurology", deptDescription="Brain treatments"),
            Department(departmentName="Orthopedics", deptDescription="Bone treatments"),
            Department(departmentName="Dermatology", deptDescription="Skin treatments"),
            Department(departmentName="Pediatrics", deptDescription="Child care"),
        ]

        db.session.add_all(departments)
        db.session.commit()

        doctor_users = User.query.filter_by(role="doctor").all()
        doctors = []

        for i in range(5):
            doctors.append(
                Doctor(
                    doctorName=f"Doctor {i+1}",
                    specialization="Specialist",
                    date=date.today(),
                    availability="Available",
                    morningSlot=True,
                    eveningSlot=True,
                    userId=doctor_users[i].id,
                    departmentId=departments[i].id
                )
            )

        db.session.add_all(doctors)
        db.session.commit()

        
        patient_users = User.query.filter_by(role="patient").all()
        patients = []

        for i in range(5):
            patients.append(
                Patient(
                    patientName=f"Patient {i+1}",
                    age=20 + i,
                    gender="Male" if i % 2 == 0 else "Female",
                    contact="9876543210",
                    userId=patient_users[i].id
                )
            )

        db.session.add_all(patients)
        db.session.commit()

        
        appointments = []

        for i in range(5):
            appointments.append(
                Appointment(
                    date=date.today(),
                    time=time(10, 0),
                    status="Booked",
                    doctor_id=doctors[i].id,
                    patient_id=patients[i].id
                )
            )

        db.session.add_all(appointments)
        db.session.commit()

        treatments = []

        for i in range(5):
            treatments.append(
                Treatment(
                    diagnosis="General Checkup",
                    prescription="Take rest",
                    notes="Stable condition",
                    medicines="Paracetamol",
                    testsDone="Blood Test",
                    visiteType="OPD",
                    appointmentId=appointments[i].id,
                    doctorId=doctors[i].id,
                    patientId=patients[i].id
                )
            )

        db.session.add_all(treatments)
        db.session.commit()

        print("✅ Database initialized with dummy data!")


if __name__ == "__main__":
    init_db()