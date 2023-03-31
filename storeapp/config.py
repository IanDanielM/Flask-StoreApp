import os,secrets
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

username=os.getenv('USERNAMEdb')
password=os.getenv('PASSWORD')
db=os.getenv('DB')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@localhost:5432/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')