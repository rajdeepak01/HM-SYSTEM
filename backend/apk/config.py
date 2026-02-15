class Config():
    Debug = False
    SQLALCHEMY_TRACK_MODIFICATION = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hms-system-database.sqlite3"
    JWT_SECRET_KEY = "@ooooooRadheKrishnaooooo!!!!!!!!!!!!!!!!RadheRadhe............!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
