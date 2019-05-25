# !/usr/bin/env python3
# importing
from flask import Flask, request, redirect, render_template
from flask import jsonify, url_for, flash, abort, g
from flask import session as login_session
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

# importing from database
from sqlalchemy import create_engine, asc
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from model import Base, User, Transaction, Rate

from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_login import logout_user
from werkzeug.utils import secure_filename

import random, string, json, time

from redis import Redis
from functools import update_wrapper
from datetime import date


# name of application
APPLICATION_NAME = "Transfer App"
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


engine = create_engine('mysql+pymysql://root:Bank2427249@localhost/transfer')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


#the user loader return the associate user object
@login_manager.user_loader
def user_loader(user_email):
	user = session.query(User).filter_by(email=user_email).one()
	if user:
                return user
	else:
		return None


# verify if user password is correct
def verify_password(email, password):
	user = session.query(User).filter_by(email=email).one()
	if not user or not user.verify_password(password):
		return None
	return user


# unauthorized user
@login_manager.unauthorized_handler
def unauthorized_handler():
        flash("You are not authorized to access this page. Please login")
        return render_template('login.html')


# login 
@app.route("/login", methods=['GET', 'POST'])
def login():
	# app.logger.info("")
        if request.method == 'POST':
                email = (request.json.get('email'))
                password = (request.json.get('password'))
                if not email or not password:
                        app.logger.warning("no info provided")
                        return jsonify({'message':'email or password not provided'}
                                       ),200#,{'Location':url_for('login')}
                else:
                        user = verify_password(email, password)
                        app.logger.info("info provided")
                        if user == None:
                                return jsonify(
                                        {'message':'user not recognized','location':url_for('login')}
                                        ),200#,{'Location':url_for('login')}
                        else:
                                login_user(user)
                                return jsonify(
                                        {'message':'successfully login','location':url_for('transfer')}
                                        ),201#, {'Location':url_for('transfer')}
        elif request.method == 'GET':
                return render_template('login.html')


# logout user
@app.route('/logout')
def logout():
        flash("Logged out successfully")
        app.logger.info("user successfully logged out")
        logout_user()
        return render_template('login.html')


# register new user
@app.route("/register", methods=['GET','POST'])
def registerUser():
        email = request.json.get('email','')
        password = request.json.get('password','')
        repassword = request.json.get('repassword')
        firstName = request.json.get('firstName','')
        lastName = request.json.get('lastName')
        title = request.json.get('title')
        if email is None or password is None:
                app.logger.info("missing arguments")
                abort(400)
        if session.query(User).filter_by(email=email).first() is not None:
                app.logger.info("existing user")
                user = session.query(User).filter_by(email=email).first()
                return jsonify(
                    {'message':'user already exists'}
                    ), 200#,{'Location':url_for('get_user', id = user.id, _external = True)}
        if password == repassword:
                user = User(email=email, firstName=firstName, lastName=lastName, title=title)
                user.hash_password(password)
                session.add(user)
                session.commit()
                return jsonify(
                    { 'email': user.email }
                    ), 201#,{'Location': url_for('get_user', id = user.id, _external = True)}
        else:
                return jsonify(
                    { 'message': 'password do not match' }
                    ), 200#,{'Location': url_for('get_user', id = user.id, _external = True)}


# get user
@app.route('/users/<int:id>')
def get_user(id):
        user = session.query(User).filter_by(id=id).one()
        if not user:
                abort(400)
        return jsonify({'email':user.email})



# transfer page
@app.route('/')
@login_required
def transfer():
    return render_template('transfer.html')


@app.route('/transfer/all')
@login_required
def getAllTransfer():
        transfer = session.query(Transaction).all()
        return jsonify({'transactions':[i.serialize for i in transfer]})


@app.route('/transfer/user')
@login_required
def getUserTransfer():
        today = str(date.today())
        app.logger.info(today)
        transfer = session.query(Transaction).filter(Transaction.user_id==current_user.id,
                                                     Transaction.transferDate >= today).all()
        return jsonify({'transactions':[i.serialize for i in transfer]})


@app.route('/transfer/<int:id>', methods=['GET','POST'])
@login_required
def singleTransfer(id):
        if request.method == 'GET':
                transfer = session.query(Transaction).filter_by(id=id).one()
        


# record and convert amout
@app.route('/convert', methods=['GET','POST'])
@login_required
def convertAmount():
        # convert amount
        usAmount = request.json.get('usamount','')
        #rate = float(request.json.get('rateSet'))
        rate = session.query(Rate).first();
        # add a if to check rate
        # calculate gd amount
        gdAmount = float(usAmount) * rate.convertRate
        transaction = Transaction(usAmount=usAmount, gdAmount=gdAmount, rate=rate.convertRate, user_id=current_user.id)
        session.add(transaction)
        session.commit()
        return jsonify({'message':'successfully added', 'gdAmount':gdAmount})


# create a new rate
@app.route('/rate', methods=['GET','POST'])
@login_required
def rateConfiguration():
        rate = session.query(Rate).first()
        if request.method == 'POST':
                newRate = request.json.get('rate')
                if rate is None:
                        rate = Rate(convertRate=newRate)
                else:
                        rate.convertRate = newRate
                session.add(rate)
                session.commit()
                return jsonify({'message':'successfully added'})
        if request.method == 'GET':
                return jsonify({'rate':rate.serialize})


@app.route('/rate/view')
@login_required
def viewRate():
        if request.method == 'GET':
                return render_template('rate.html')

                


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase +
                                                     string.digits)
                                       for x in range(32))
    app.run(host='0.0.0.0', port=5000)


