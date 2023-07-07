from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin     # for login_manager
from datetime import datetime

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=True)
    college_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    deadline = db.Column(db.DateTime)
    application_fee = db.Column(db.Float)
    pending_document = db.Column(db.String(200))
    requirement = db.Column(db.String(200))
    waiver = db.Column(db.String(200), default='No')
    submitted_document = db.Column(db.String(200))
    country = db.Column(db.String(200))
    degree = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)

    def __repr__(self):
        return f"Application('{self.applicant_name}', '{self.college_name}', '{self.status}')"
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True , nullable=False)    # unique=True means that no two users can have the same username
    username = db.Column(db.String(30), unique=True , nullable=False)    # unique=True means that no two users can have the same username
    password = db.Column(db.String(30),nullable=False)
    applications = db.relationship('Application', backref='user',lazy=True)    # 'Application' is the table name
    def __repr__(self):
        return f"User('{self.username}')"
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
