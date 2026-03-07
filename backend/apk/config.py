from celery.schedules import crontab

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hms-system-database.sqlite3"

    JWT_SECRET_KEY = "==oooooopppppppppRadheKrishna======="

    CELERY = {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/0",
        "task_ignore_result": False,

        "beat_schedule": {

            "daily-reminder": {
            "task": "daily_patient_reminder",
            "schedule": crontab(minute="*")
            },
            # day_of_month=1, hour=9, minute=0 for monthly report 
            # hour=8, minute=0 for per day at 8 Am
            "monthly-report": {
            "task": "monthly_doctor_report",
            "schedule": crontab(minute="*")
            }
        }
    }

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "donotreply@hms.com"