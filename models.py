from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin , db.Model):
    __tablename__ = 'userstore'
    id           = db.Column(db.Integer, primary_key=True)
    user_login   = db.Column(db.String(35),unique=True)
    password     = db.Column(db.String(100))
    type         = db.Column(db.String(10))
    timestamp    = db.Column(db.DateTime)

    def __init__(self, user_login, type):
        self.user_login = user_login
        self.type = type

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)




class Customer(db.Model):
    __tablename__ = 'customer'
    ws_ssn      = db.Column(db.Integer, unique=True)
    ws_cust_id  = db.Column(db.Integer, primary_key=True)
    ws_name     = db.Column(db.String(20))
    ws_adrs     = db.Column(db.String(50))
    ws_age      = db.Column(db.Integer)

    def __init__(self, ws_ssn, ws_name, ws_adrs,ws_age):
        self.ws_ssn = ws_ssn
        self.ws_name = ws_name
        self.ws_adrs = ws_adrs
        self.ws_age = ws_age



class Account(db.Model):
    ws_acc_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_cust_id          = db.Column(db.Integer)
    ws_acct_type        = db.Column(db.String(1))
    ws_acct_balance     = db.Column(db.Integer)
    ws_acct_crdate      = db.Column(db.Date)
    ws_acct_lasttrdate  = db.Column(db.Date)
    ws_acct_duration    = db.Column(db.Integer)

    def __init__(self, ws_cust_id, ws_acct_type):
        self.ws_cust_id   = ws_cust_id
        self.ws_acct_type = ws_acct_type
      

#CustomerStatus table columns – SSN ID, Customer ID, Status, Message, Last Updated

class CustomerStatus(db.Model):
    status_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_ssn          = db.Column(db.Integer)
    ws_cust_id      = db.Column(db.Integer)
    status          = db.Column(db.String(15))
    message         = db.Column(db.String(25))
    last_updated    = db.Column(db.Date)

    def __init__(self, ws_ssn , ws_cust_id, status,message):
        self.ws_ssn       = ws_ssn
        self.ws_cust_id   = ws_cust_id
        self.status       = status
        self.message      = message

#AccountStatus table columns – Customer ID, Account ID, Account Type, Status, Message, Last Updated

class AccountStatus(db.Model):
    status_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_acc_id       = db.Column(db.Integer)
    ws_cust_id      = db.Column(db.Integer)
    ws_acct_type    = db.Column(db.String(1))
    status          = db.Column(db.String(15))
    message         = db.Column(db.String(25))
    last_updated    = db.Column(db.Date)

    def __init__(self, ws_acc_id , ws_cust_id, ws_acct_type ,status, message):
        self.ws_acc_id    = ws_acc_id
        self.ws_cust_id   = ws_cust_id
        self.ws_acct_type = ws_acct_type
        self.status       = status
        self.message      = message


class Transaction(db.Model):
    trxn_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_acc_id       = db.Column(db.Integer)
    ws_cust_id      = db.Column(db.Integer)
    ws_acct_type    = db.Column(db.String(1))
    ws_amt          = db.Column(db.Integer)
    ws_trxn_date    = db.Column(db.Date)
    ws_src_typ      = db.Column(db.String(1))
    ws_tgt_typ      = db.Column(db.String(1))
    cr_or_db        = db.Column(db.String(7))
    description     = db.Column(db.String(50))

    def __init__(self, ws_acc_id , ws_cust_id, ws_amt,ws_acct_type ,ws_src_typ, ws_tgt_typ,cr_or_db):
        self.ws_acc_id    = ws_acc_id
        self.ws_cust_id   = ws_cust_id
        self.ws_amt       = ws_amt
        self.ws_acct_type = ws_acct_type
        self.ws_src_typ   = ws_src_typ
        self.ws_tgt_typ   = ws_tgt_typ
        self.cr_or_db     = cr_or_db
