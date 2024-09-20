import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'default_connection_string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
