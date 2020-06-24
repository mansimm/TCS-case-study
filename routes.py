from datetime import datetime
from app import db,app
import random
from sqlalchemy import and_

import pdfkit
pdfkit.from_url("http://google.com", "statements.pdf")

from forms import SignUpForm,LoginForm,CreateCustomerForm, PullCustomer, FindCustomer, CreateAccountForm, FindAccount, GetAccount
from forms import DepositeForm ,WithdrawForm, TransferForm, GetStatementFrom


from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response

from models import User, Customer, Account, CustomerStatus, AccountStatus,Transaction



@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("base.html", index=True)



@app.route("/signup",methods=['GET','POST'])
def signup():
    form = SignUpForm()
    
    if form.validate_on_submit()== True:        
        user_login  = form.user_login.data
        password    = form.password.data
        type        = form.type.data

        user = User.query.filter_by(user_login = user_login).first()
        if user:
            flash("This email is already in use , please use another.","danger")
            return redirect("/signup")

        user = User(user_login=user_login,type=type)
        user.set_password(password)
        user.timestamp = datetime.now()
        db.session.add(user)
        db.session.commit()     
        db.session.flush()            

        flash(f"{user_login}, You are successfully registered !","success")
        return redirect("/login")    
    return render_template("signup.html",title="Sign Up",form=form,signup=True)



@app.route("/login",methods=['GET','Post'])
def login():
    if session.get('user_name'):
        redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit()== True:
       user_login    = form.user_login.data
       password      = form.password.data
       type          = form.type.data

       #password = get_password(password)

       user= User.query.filter_by(user_login=user_login, type=type).first()
       if user and user.get_password(password) :

           flash(f"{user.user_login} ,You are successfully logged in !", "success")
           #flash("You are successfully login !", "success")
           session['user_id']   = user.id
           session['user_name'] = user.user_login
           session['user_type'] = user.type

           if user.type == 'executive':
               return redirect("/customer")
           elif user.type == 'cashier':
               return redirect("/customer")
               
       else:
            flash("Sorry, something went wrong !", "danger")

           

    return render_template("login.html",title='Employee Login',form=form,login=True)


@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('user_name',None)
    session.pop('user_type',None)
    return redirect(url_for('index'))



@app.route("/create_customer",methods=['GET','POST'])
def create_customer():
    if session['user_type'] == 'executive':
        render_template('customer.html')

        
    form = CreateCustomerForm()

    if form.validate_on_submit() == True:
        ws_ssn = form.ws_ssn.data
        ws_name = form.ws_name.data
        ws_adrs = form.ws_adrs.data
        ws_age  = form.ws_age.data

        customer = Customer.query.filter_by(ws_ssn=ws_ssn).first()

        if not customer:
            customer = Customer(ws_ssn=ws_ssn ,ws_name=ws_name ,ws_adrs=ws_adrs ,ws_age=ws_age)
            db.session.add(customer)
            db.session.commit()

            update_status_customer(ws_ssn,'created')
            flash("Customer creation initiated successfully","success")
            return render_template("customer.html",title='Customer Created',create_customer=True)
        else:
            flash("Something went wrong !", "danger")
    
    return render_template("create_customer.html",form=form,create_customer=True,title='Create Customer')



@app.route("/pull_customer",methods=['GET','POST'])
def pull_customer():
    form = PullCustomer()

    if form.validate_on_submit()== True:
        ws_ssn = form.ws_ssn.data
        ws_cust_id = form.ws_cust_id.data

        if  ws_ssn :
            customer = Customer.query.filter_by(ws_ssn=ws_ssn).all()
            if customer:
                flash("Customer found","success")
                return render_template("delete_customer.html",delete_customer=True,customers=customer)
            else:
                flash("Customer not found !","danger")
        elif ws_cust_id:
            customer = Customer.query.filter_by(ws_cust_id=ws_cust_id).all()
            if customer:
                flash("Customer found","success")
                return render_template("delete_customer.html",delete_customer=True,customers=customer)
            else:
                flash("Customer not found !","danger")
        else:
            flash('Atleast one of these mandatory.','danger')
            

        '''
        #customer = Customer.query.filter_by(ws_ssn=ws_ssn,ws_cust_id=ws_cust_id).all()
        if customer:
            flash("Customer found","success")
            return render_template("delete_customer.html",delete_customer=True,customers=customer)
        else:
            flash("Customer not found !","danger")
        '''

    return render_template("pull_customer.html",form=form,delete_customer=True,title="Find Customer")


@app.route("/delete_customer",methods=['GET','POST'])
def delete_customer():
    ws_ssn = request.form.get('ws_ssn')
    ws_name = request.form.get('ws_name')
    ws_adrs = request.form.get('ws_adrs')
    ws_age = request.form.get('ws_age')

    customer = Customer.query.filter_by(ws_ssn=ws_ssn, ws_name=ws_name, ws_adrs=ws_adrs).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        update_status_customer(ws_ssn,'deleted')
        flash(f"{ws_name} is deleted !", "success")
        return render_template("customer.html",title="Deleted Customer",delete_customer=True)
    else:
        flash("Something went wrong !","danger")
    return render_template("delete_customer.html",title="Delete customer",delete_customer=True)



@app.route("/find_customer",methods=['GET','POST'])
def find_customer():
    form = FindCustomer()
    
    if form.validate_on_submit()== True:
        ws_ssn = form.ws_ssn.data
        ws_cust_id = form.ws_cust_id.data


        if  ws_ssn :
            customer = Customer.query.filter_by(ws_ssn=ws_ssn).first()
            if customer:
                flash("Customer found","success")
                return render_template("update_customer.html",update_customer=True,customer=customer)
            else:
                flash("Customer not found !","danger")
        elif ws_cust_id:
            customer = Customer.query.filter_by(ws_cust_id=ws_cust_id).first()
            if customer:
                flash("Customer found","success")
                return render_template("update_customer.html",update_customer=True,customer=customer)
            else:
                flash("Customer not found !","danger")
        else:
            flash('Atleast one of these mandatory.','danger')
            
        '''
        customer = Customer.query.filter_by(ws_ssn=ws_ssn,ws_cust_id=ws_cust_id).first()
        if customer:
            flash("Customer found","success")
            return render_template("update_customer.html",update_customer=True,customer=customer)
        else:
            flash("Customer not found !","danger")
        '''    
    return render_template("find_customer.html",form=form,update_customer=True,title='Find Customer')



@app.route("/update_customer",methods=["GET","POST"])
def update_customer():
    if request.method == 'POST' :
        ws_ssn = request.form.get('ws_ssn')
        ws_name = request.form.get('ws_name')
        ws_adrs = request.form.get('ws_adrs')
        ws_age = request.form.get('ws_age')

        if not ws_name:
           flash("Please enter name !","danger")
        elif not ws_adrs:
           flash("Please enter address !","danger")
        elif not ws_age:
           flash("Please enter age !","danger")
        elif not ws_ssn:
            flash("Please enter ssn id !","danger")
        else:
            customer = Customer.query.filter_by(ws_ssn = ws_ssn).first()
            if customer:
                customer.ws_name = ws_name
                customer.ws_adrs = ws_adrs
                customer.ws_age  = ws_age

                db.session.commit()
                update_status_customer(ws_ssn,'updated')
                flash(f"{ws_name} is updated !", "success")
                return render_template("customer.html",title="Updated Customer",update_customer=True)
            else:
                flash("Something went wrong !","danger")
        
    return render_template("update_customer.html",update_customer=True, title="Update Customer")


@app.route("/create_account", methods=['GET','POST'])
def create_account():
    form = CreateAccountForm()
    if request.method == 'POST':
        ws_cust_id   = request.form.get('ws_cust_id')
        ws_acct_type = request.form.get('ws_acct_type')
        ws_amt       = request.form.get('ws_amt')

        customer = Customer.query.filter_by(ws_cust_id=ws_cust_id).first()
        if customer:
            account = Account(ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type)
            account.ws_acct_balance = ws_amt
            account.ws_acct_crdate  = datetime.now()
            account.ws_acct_lasttrdate = datetime.now()
            #ws_acct_duration

            db.session.add(account)
            db.session.commit()
            # to update status
            temp_acc = Account.query.order_by(Account.ws_acc_id.desc()).first()
            if temp_acc:
                update_status_account(temp_acc.ws_acc_id,'created')

            flash("Account creation initiated !","success")
            return render_template("customer.html",title="Account created",create_account=True)
        else:
            flash("Customer Id does not exist !","danger")

    return render_template("create_account.html",form=form,create_account=True,title='Create Account')



@app.route("/find_account",methods=['GET','POST'])
def find_account():
    form = FindAccount()
    if request.method == 'POST':
        if form.validate_on_submit()== True:
            ws_ssn = form.ws_ssn.data
            ws_cust_id = form.ws_cust_id.data

            
            if  ws_ssn :
                customer = Customer.query.filter_by(ws_ssn=ws_ssn).first()
                if customer:
                    ws_cust_id = customer.ws_cust_id
                    account = Account.query.filter_by(ws_cust_id=ws_cust_id).all()
                    if account:
                        flash("Account found","success")
                        return render_template("delete_account.html",delete_account=True,accounts=account)
                    else:
                        flash("Account not found !","danger")
                else:
                    flash("Customer with this customer id does not exist !","danger")

            elif ws_cust_id:
                account = Account.query.filter_by(ws_cust_id=ws_cust_id).all()
                if account:
                    flash("Account found","success")
                    return render_template("delete_account.html",delete_account=True,accounts=account)
                else:
                    flash("Account not found !","danger")
            else:
                flash('Atleast one of these mandatory.','danger')      
            
    return render_template("find_account.html",form=form,delete_account=True,title='Find Account')




@app.route("/delete_account", methods=['GET','POST'])
def delete_account():
    if request.method == 'POST':
        ws_acc_id = request.form.get('ws_acc_id')
        ws_cust_id = request.form.get('ws_cust_id')
       
        account = Account.query.filter_by(ws_acc_id=ws_acc_id, ws_cust_id=ws_cust_id).first()
        if account:
            db.session.delete(account)
            db.session.commit()

            # for status update
            update_status_account(ws_acc_id,'deleted')
            flash(f"{ws_acc_id} is deleted !", "success")
            return render_template("delete_account.html",title="Deleted Customer",delete_account=True)
        else:
            flash("Something went wrong !","danger")
    return render_template("delete_account.html",delete_account= True)


@app.route("/status")
def status():
    return render_template("status.html",status=True)

@app.route("/account_status")
def account_status():
    accounts = AccountStatus.query.all()
    return render_template("account_status.html",status=True,accounts=accounts)

@app.route("/customer_status")
def customer_status():
    customers = CustomerStatus.query.all()
    return render_template("customer_status.html",status=True,customers=customers)

@app.route("/customer")
def customer():
    if session.get('user_name'):
        return render_template("customer.html",customer=True)




############################ Functions to update status ###########################################
def update_status_customer(ws_ssn1,status):
    customer = Customer.query.filter_by(ws_ssn=ws_ssn1).first()
    if customer :
        ws_ssn= customer.ws_ssn
        ws_cust_id= customer.ws_cust_id

        if status == 'created':
            cust_status = CustomerStatus(ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,status='Created',message='Completed')
            cust_status.last_updated= datetime.now()
            db.session.add(cust_status)
            db.session.commit()
            db.session.flush()
        elif status =='updated':
            cust_status = CustomerStatus.query.filter_by(ws_ssn=ws_ssn).first()
            if cust_status:
                cust_status.status = 'Updated'
                cust_status.message = 'Completed'
                cust_status.last_updated = datetime.now()
                db.session.commit()            
    else:
        cust_status = CustomerStatus.query.filter_by(ws_ssn=ws_ssn1).first()
        if cust_status:
            cust_status.status = 'Deleted'
            cust_status.message = 'Completed'
            cust_status.last_updated = datetime.now()
            db.session.commit()  


def update_status_account(acc_id,status):
    if(acc_id):
        if status == 'created' :
            acc = Account.query.filter_by(ws_acc_id=acc_id).first()
            if acc :
                account_status = AccountStatus(ws_acc_id = acc.ws_acc_id, ws_cust_id = acc.ws_cust_id ,ws_acct_type = acc.ws_acct_type, status='Created',message='Completed')
                account_status.last_updated = datetime.now()
                db.session.add(account_status)
                db.session.commit()

        else:
            account_status = AccountStatus.query.filter_by(ws_acc_id=acc_id).first()
            if account_status:
                account_status.status = 'Deleted'
                account_status.message = 'Completed'
                account_status.last_updated = datetime.now()
                db.session.commit()
            

##########################################################################################################
##################################  Chashier #################################################
#############################################################################################

@app.route("/get_accounts", methods=['GET','POST'])
def get_accounts():
    form = GetAccount()
    if request.method == 'POST':
        if form.validate_on_submit():
            input_type = form.input_type.data
            input      = form.input.data

            if input_type == 'ssn' or input_type=='cust_id':
                if input_type == 'ssn':
                    ssn=input
                    cust = Customer.query.filter_by(ws_ssn=ssn).first()
                    cust_id = cust.ws_cust_id
                else:
                    cust_id = input
                accounts = Account.query.filter_by(ws_cust_id = cust_id).all()
                if accounts:
                    return render_template("get_accounts.html",get_accounts=True,title='Accounts',accounts = accounts)
                else:
                    flash("Account not found... Please check id !","danger")
            else:
                account = Account.query.filter_by(ws_acc_id=input).first()
                if account:
                    return render_template("account_details.html",account=account,title='Account Details',get_accounts=True)
                else:
                    flash("Account not found... Please check account id !","danger")

    return render_template("get_accounts.html",get_accounts=True,form=form,title='Get Accounts')



@app.route("/deposite/<acc_id>",methods=['GET','POST'])
def deposite(acc_id):
    form = DepositeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            amt = form.amt.data
            account = Account.query.filter_by(ws_acc_id=acc_id).first()
            x = int(account.ws_acct_balance)
            account.ws_acct_balance = x + int(amt)
            db.session.commit()
            flash("Amount deposited successfully","success")

            transaction = Transaction(ws_acc_id=account.ws_acc_id ,ws_cust_id=account.ws_cust_id,
                                        ws_amt=amt, ws_acct_type=account.ws_acct_type,
                                        ws_src_typ=None,ws_tgt_typ=None,cr_or_db='Credit')
            transaction.ws_trxn_date = datetime.now() 
            transaction.description  = ''+str(amt)+' credited in '+str(account.ws_acc_id)+' account'                     
            db.session.add(transaction)
            db.session.commit()

            return render_template("deposite.html",account=account,old_balance=x,get_accounts=True)
            
    return render_template("deposite.html",title='Deposite Amount',form=form,get_accounts=True)

@app.route("/withdraw/<acc_id>",methods=['GET','POST'])
def withdraw(acc_id):
    form = WithdrawForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            amt = form.amt.data
            account = Account.query.filter_by(ws_acc_id=acc_id).first()
            x = int(account.ws_acct_balance)
            if(x < int(amt)):
                flash("Your Balance is not sufficient to withdraw !","danger")
            else:
                account.ws_acct_balance = x - int(amt)
                db.session.commit()
                flash("Amount withdrawed successfully .","success")
                
                transaction = Transaction(ws_acc_id=account.ws_acc_id ,ws_cust_id=account.ws_cust_id,
                                        ws_amt=amt, ws_acct_type=account.ws_acct_type,
                                        ws_src_typ=None,ws_tgt_typ=None,cr_or_db='Debit')
                transaction.ws_trxn_date = datetime.now() 
                transaction.description  = ''+str(amt)+' debited from '+ str(account.ws_acc_id)+' account'                       
                db.session.add(transaction)
                db.session.commit()

                return render_template("withdraw.html",account=account,old_balance=x,get_accounts=True)

    return render_template("withdraw.html",title='Withdraw Amount',form=form)


@app.route("/transfer",methods=['POST','GET'])
def transfer():
    form = TransferForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            src_acc_id = form.src_acc_id.data
            tar_acc_id = form.tar_acc_id.data
            amount     = form.amount.data

            src_acc = Account.query.filter_by(ws_acc_id= src_acc_id).first()
            tar_acc = Account.query.filter_by(ws_acc_id= tar_acc_id).first()

            if src_acc and tar_acc :
                x = int(src_acc.ws_acct_balance)
                y = int(tar_acc.ws_acct_balance)
                z = int(amount)
                if x < z :
                    flash("Transfer not allowed, please choose smaller amount","danger")
                else :
                    src_acc.ws_acct_balance = x - z
                    src_acc.acct_lasttrdate = datetime.now()
                    tar_acc.ws_acct_balance = y + z
                    tar_acc.acct_lasttrdate = datetime.now()
                    db.session.commit()
                    flash("Amount transfer completed successfully","success")

                    #for sourse account
                    transaction = Transaction(ws_acc_id=src_acc.ws_acc_id ,ws_cust_id=src_acc.ws_cust_id,
                                        ws_amt=amount, ws_acct_type=src_acc.ws_acct_type,
                                        ws_src_typ=src_acc.ws_acct_type,ws_tgt_typ=tar_acc.ws_acct_type,cr_or_db='Debit')
                    transaction.ws_trxn_date = datetime.now() 
                    transaction.ws_src_typ   = src_acc.ws_acct_type
                    transaction.ws_tgt_typ   = tar_acc.ws_acct_type
                    transaction.description  = ''+amount+' transfered from '+ str(src_acc.ws_acc_id)+' to '+str(tar_acc.ws_acc_id)                       
                    db.session.add(transaction)
                    db.session.commit()
                    #for destination
                    transaction = Transaction(ws_acc_id=tar_acc.ws_acc_id ,ws_cust_id=tar_acc.ws_cust_id,
                                        ws_amt=amount, ws_acct_type=tar_acc.ws_acct_type,
                                        ws_src_typ=src_acc.ws_acct_type,ws_tgt_typ=tar_acc.ws_acct_type,cr_or_db='Credit')
                    transaction.ws_trxn_date = datetime.now() 
                    transaction.ws_src_typ   = src_acc.ws_acct_type
                    transaction.ws_tgt_typ   = tar_acc.ws_acct_type
                    transaction.description  = ''+amount+' transfered from '+ str(src_acc.ws_acc_id)+' to '+str(tar_acc.ws_acc_id)                       
                    db.session.add(transaction)
                    db.session.commit()

                    return render_template('transfer.html',src_acc=src_acc,tar_acc=tar_acc,title='Transfer',x=x,y=y,get_accounts=True)
            elif not src_acc:
                flash("Source account not found !","danger")
            elif not tar_acc:
                flash("Target account not found !","danger")
            else:
                flash("Something went wrong ....",'danger')

    return render_template("transfer.html",form=form, title="Transfer",get_accounts=True)


@app.route("/statements",methods=['POST','GET'])
def statements():
    if request.method == 'POST':
        ws_acc_id = request.form.get('ws_acc_id')
        option    = request.form.get('option')
        if option == 'option_1':
            last_n_tran = request.form.get('last_n_tran')
            transactions = Transaction.query.filter_by(ws_acc_id=ws_acc_id).order_by(Transaction.ws_acc_id.desc()).limit(last_n_tran)
            transactions = transactions[::-1]
            if transactions :
                return render_template('statements.html',transactions=transactions,statements=True,title='Get Statements')
            else:
                flash("Sorry, no transactions to show !","danger")
   
        elif option == 'option_2':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            transactions = Transaction.query.filter_by(ws_acc_id=ws_acc_id ).filter(Transaction.ws_trxn_date.between( start_date, end_date)).all()
            if transactions:
                return render_template('statements.html',transactions=transactions,statements=True,title='Get Statements')
            else:
                flash("Sorry, no transactions to show !","danger")
        else :
            flash("Select one of these","danger")



    return render_template("statements.html", statements=True,title='Get Statements')



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",aboutus=True,title='About us')

@app.route("/contacts")
def contacts():
    return render_template("contacts.html",contacts=True,title='Contacts')

'''

@app.route("/download_pdf/<transactions>",methods=['POST','GET'])
def download_pdf(transactions):
    if request.method == 'POST':
        if transactions:
            flash(f"id={transactions}")
            id=0
            for trans in transactions:
                id = trans.ws_acc_id
                break
            temp = Transaction.query.filter_by(ws_acc_id = id).all()
            return render_template('statements.html',transactions = temp)
            
            rendered = render_template("pdf.html",transactions=transactions)
            pdf = pdfkit.from_string( rendered, False)
            response = make_response(pdf)
            response.headers['Content-Type']='application/pdf'
            response.headers['Content-Desposition'] = 'inline; filename=statements.pdf'
            return response
            
        else:
            flash("transactin not present","danger")
            return render_template('pdf.html')
'''