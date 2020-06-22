from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_ENGINE = 'mysql+pymysql'
DB_USERNAME = 'root'
DB_PASSWORD = 'mansi@1999'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'tcscasestudy'


app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_ENGINE + '://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME

db = SQLAlchemy(app)
from models import User,Customer,Account,CustomerStatus,AccountStatus,Transaction
import routes
