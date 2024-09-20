import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'g!kS9Pn3$2w!b7D9Fz&Qx@A1LmY#uVcH')

    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "mssql+pyodbc://@BRSBESQLCORP54D/DB_CARFORD?driver=SQL+Server+Native+Client+11.0&trusted_connection=yes")
  