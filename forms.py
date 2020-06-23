from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,IntegerField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, NumberRange, Optional
from models import User,Customer
from wtforms_validators import AlphaSpace, AlphaNumeric, Integer
from flask_datepicker import datepicker

class LoginForm(FlaskForm):
    user_login       = StringField("Login", validators=[DataRequired(), Email() ],render_kw={"placeholder": "Enter login"})
    password         = PasswordField("Password", validators=[DataRequired(), Length(min=5,max=16)] ,render_kw={"placeholder": "Enter password"})
    type             = SelectField("Type", choices=[('executive','Customer Executive'),('cashier','Cashier')],validators=[DataRequired(), Length(min=5,max=16)])
    remember_me      = BooleanField("Remember Me")
    submit           = SubmitField("Login")

class SignUpForm(FlaskForm):
    user_login       = StringField("Email", validators=[DataRequired(), Email() ] ,render_kw={"placeholder": "Enter login"})
    password         = PasswordField("Password", validators=[DataRequired(), Length(min=5,max=16)] ,render_kw={"placeholder": "Enter password"})
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=5,max=16), EqualTo('password')],render_kw={"placeholder": "Enter password again"})
    type             = SelectField("Type", choices=[('executive','Customer Executive'),('cashier','Cashier')],validators=[DataRequired(), Length(min=5,max=16)])
    submit           = SubmitField("Sign Up")
    
class CreateCustomerForm(FlaskForm):
    ws_ssn           = StringField("SSN Id", validators=[DataRequired(),Integer(),Length(min=9,max=9) ],render_kw={"placeholder": "Enter SSN Id"})
    ws_name          = StringField("Customer Name", validators=[DataRequired(), Length(min=2,max=55), AlphaSpace() ],render_kw={"placeholder": "Enter customer name"})
    ws_adrs          = TextAreaField("Address", validators=[DataRequired(), Length(min=5,max=160) ],render_kw={"placeholder": "Enter address"})#AlphaNumeric()
    ws_age           = StringField("Age", validators=[DataRequired(),Integer() ],render_kw={"placeholder": "Enter age"})
    submit           = SubmitField("Create")
    


class PullCustomer(FlaskForm):
    ws_ssn           = StringField("SSN Id", validators=[ Optional(),Integer(),Length(min=9,max=9) ],render_kw={"placeholder": "Enter SSN Id"})
    ws_cust_id       = StringField("Customer Id", validators=[ Optional(), Integer() ],render_kw={"placeholder": "Enter customer Id"})
    submit           = SubmitField("Search")


class FindCustomer(FlaskForm):
    ws_ssn           = StringField("SSN Id", validators=[Optional(),Integer(),Length(min=9,max=9) ],render_kw={"placeholder": "Enter SSN Id"})
    ws_cust_id       = StringField("Customer Id", validators=[Optional(), Integer() ] ,render_kw={"placeholder": "Enter customer Id"})
    submit           = SubmitField("Search")


class UpdateCustomer(FlaskForm):
    ws_ssn           = StringField("SSN Id", validators=[DataRequired(),Integer(),Length(min=9,max=9) ])
    ws_name          = StringField("Customer Name", validators=[DataRequired(), Length(min=2,max=55), AlphaSpace() ])
    ws_adrs          = TextAreaField("Address", validators=[DataRequired(), Length(min=5,max=160), AlphaNumeric() ])
    ws_age           = StringField("Age", validators=[DataRequired(),Integer() ])
    submit           = SubmitField("Create")
    
class CreateAccountForm(FlaskForm):
    ws_cust_id       = StringField("Customer Id", validators=[DataRequired(),Integer(),Length(min=9,max=9) ],render_kw={"placeholder": "Enter customer Id"})
    ws_acct_type     = SelectField("Account Type", choices=[('s','Savings Account'),('c','Current Account')],validators=[DataRequired(), Length(min=5,max=16)])
    ws_amt           = StringField("Deposite Amount", validators=[DataRequired(),Integer(),Length(min=1,max=15) ],render_kw={"placeholder": "Enter amount"})
    submit           = SubmitField("Create")

class FindAccount(FlaskForm):
    ws_ssn           = StringField("SSN Id", validators=[Optional(),Integer(),Length(min=9,max=9) ] ,render_kw={"placeholder": "Enter SSN Id"})
    ws_cust_id       = StringField("Customer Id", validators=[Optional(), Integer() ,Length(min=1,max=9)],render_kw={"placeholder": "Enter customer Id"})
    submit           = SubmitField("Search")


##################################  for cashier #####################################################

class GetAccount(FlaskForm):
    input_type       = SelectField("Input Type", choices=[('ssn','SSN Id'),('cust_id','Customer Id'), ('acc_id','Account Id')],validators=[DataRequired()])
    input            = StringField("Input", validators=[DataRequired(),Integer(),Length(min=1,max=9) ])
    submit           = SubmitField("Search")

class DepositeForm(FlaskForm):
    amt              = StringField("Deposite Amount", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter amount"})
    submit           = SubmitField("Deposite")

class WithdrawForm(FlaskForm):
    amt              = StringField("Withdraw Amount", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter amount"})
    submit           = SubmitField("Withdraw")

class TransferForm(FlaskForm):
    src_acc_id       = StringField("Source Account Id", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter source account id"})
    tar_acc_id       = StringField("Target Account Id", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter target account id"})
    amount           = StringField("Amount", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter amount"})
    submit           = SubmitField("Transfer")

class GetStatementFrom(FlaskForm):
    ws_acc_id        = StringField("Account Id", validators=[DataRequired(),Integer(),Length(min=1,max=9) ],render_kw={"placeholder": "Enter account Id"})
    last_n_tran      = SelectField("Last N Transactions", choices=[('1','1'),('2','2'), ('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')],validators=[Optional()])
    start_date       = DateField("Start Date",validators=[DataRequired()], format = '%d/%m/%Y')
    end_date         = DateField("End Date")
    submit           = SubmitField("Submit")

