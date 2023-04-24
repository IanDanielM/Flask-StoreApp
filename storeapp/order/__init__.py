from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets,os

app = Flask(__name__)
app.config['SECRET_KEY']=secrets.token_hex(16)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel:iamiandaniel@localhost:5432/storeapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)






