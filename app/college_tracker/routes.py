from flask import  Blueprint,Response, render_template, request, flash, redirect, url_for, abort,send_file
from flask_login import login_required, current_user,login_user, logout_user    # for login_manager
from .extensions import db, login_manager
from .model import Application,User
from datetime import datetime
# from .models import Demo
# from .utils.views import get_greeting,generate_demo_url
# from flask_caching import Cache
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
# import validators
# import secrets
# import qrcode
import io



tracker = Blueprint('tracker', __name__)
# cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
# limiter = Limiter(key_func=get_remote_address)

@tracker.route('/')
@login_required
def index():
    return render_template('index.html')
#URL User Authentication and Authorisation (login,logout,signup)Routes
# signup route
@tracker.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username already exists.', 'danger')
            return redirect(url_for('tracker.signup'))
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email address already exists.', 'danger')
            return redirect(url_for('tracker.signup'))

        user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
        try:
            user.save()
        except:
            db.session.rollback()
            response = {'Message': 'Unexpected error occurred while saving'}
            return response, 500

        flash('Account created successfully!', 'success')
        return redirect(url_for('tracker.index'))

    return render_template('signup.html')
# login route   
@tracker.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tracker.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('tracker.login'))
        login_user(user)
        return redirect(url_for('tracker.index'))
     # Return a response when the request method is not 'POST'
    return render_template('login.html')
#logout route
@tracker.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('tracker.login'))
#
#delete account route 
# @tracker.route('/delete_account', methods=['GET', 'POST'])
# @login_required
# def delete_account():
#     if request.method == 'POST':
#         user = User.query.filter_by(email=current_user.email).first()
#         if user:
#             # Delete the associated URLs
#             urls = Url.query.filter_by(user=user).all()
#             for url in urls:
#                 db.session.delete(url)

#             # Delete the user account
#             db.session.delete(user)
#             db.session.commit()

#             # Log out the user
#             logout_user()

#             flash('Your account has been deleted.', 'success')
#             return redirect(url_for('url.index'))
#         else:
#             flash('User not found.', 'danger')
#             return redirect(url_for('url.delete_account'))

#     # # GET request
#     # return render_template('delete_user_account.html')
#Route for adding a new application
@tracker.route('/add', methods=['GET', 'POST'])
def add_application():
    
    college_name = request.form.get('college_name')
    status = request.form.get('status')
        # applicant_name = request.form.get('applicant_name')
    deadline_str = request.form.get('deadline')
    deadline= datetime.strptime(deadline_str,'%Y-%m-%d').date()
    
    application_fee = request.form.get('application_fee')
    waiver = request.form.get('waiver')
    pending_document = request.form.get('pending_document')
    submitted_document = request.form.get('submitted_document')
    country = request.form.get('country')
    requirement = request.form.get('requirement')
    degree= request.form.get('degree')
        
    application = Application(college_name=college_name, status=status, country=country,requirement=requirement,degree=degree, deadline=deadline, application_fee=application_fee,  waiver=waiver,pending_document=pending_document, submitted_document=submitted_document)
    application.save()
      
    #return render_template('result.html', college_name=application.college_name, status=application.status, country=application.country,requirement=application.requirement,degree=application.degree, deadline=application.deadline, application_fee=application.application_fee, waiver=application.waiver, pending_document=application.pending_document, submitted_document=application.submitted_document)
    return redirect(url_for('tracker.result' , college_name=application.college_name ,status=application.status, country=application.country,requirement=application.requirement,degree=application.degree, deadline=application.deadline, application_fee=application.application_fee, waiver=application.waiver, pending_document=application.pending_document, submitted_document=application.submitted_document))
@tracker.route('/results')
@login_required
def result():
    user = current_user.id
    applications = Application.query.filter_by(user_id=user).all()
    return render_template('result.html' , applications=applications)
#Route for editing an application
@tracker.route('/edit')
@login_required
def edit():
    pass
