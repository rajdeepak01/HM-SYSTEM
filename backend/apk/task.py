import csv
import os
from datetime import datetime, date
from celery import shared_task
from flask import current_app

from .models import Treatment, Doctor, Appointment
from .mail_utils import send_email
from .email_template import render_email_template
import pytz


@shared_task(name="export_patient_csv")
def export_patient_csv(patient_id):

    export_folder = os.path.join(current_app.root_path, "static", "exports")

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    filename = f"patient_{patient_id}_treatments.csv"
    filepath = os.path.join(export_folder, filename)

    treatments = Treatment.query.filter_by(patientId=patient_id).all()

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "patient_id",
            "doctor_name",
            "appointment_date",
            "diagnosis",
            "prescription",
            "visit_type"
        ])

        for t in treatments:

            doctor = Doctor.query.get(t.doctorId)
            appointment = Appointment.query.get(t.appointmentId)

            writer.writerow([
                patient_id,
                doctor.doctorName if doctor else None,
                appointment.date.isoformat() if appointment else None,
                t.diagnosis,
                t.prescription,
                t.visiteType
            ])

    return f"/static/exports/{filename}"

@shared_task(name="daily_patient_reminder")
def daily_patient_reminder():
    ist = pytz.timezone("Asia/Kolkata")

    today = datetime.now(ist).date()

    appointments = Appointment.query.filter_by(date=today).all()

    for appt in appointments:

        patient = appt.patient
        doctor = appt.doctor

        message = f"""
        <h3>Appointment Reminder</h3>

        Hello {patient.patientName},

        You have an appointment today.

        <b>Doctor:</b> {doctor.doctorName} <br>
        <b>Time:</b> {appt.time}
        """

        send_email(
            patient.user.email,
            "Hospital Appointment Reminder",
            message
        )

    return f"{len(appointments)} reminders sent"

@shared_task(name="monthly_doctor_report")
def monthly_doctor_report():

    doctors = Doctor.query.all()

    for doctor in doctors:

        appointments = Appointment.query.filter_by(
            doctor_id=doctor.id
        ).all()

        html = render_email_template(
            doctor.doctorName,
            appointments
        )

        send_email(
            doctor.user.email,
            "Monthly Doctor Activity Report",
            html
        )

    return "Monthly reports sent !!!!! :)"