from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    internships = db.relationship('Internship', backref='owner', lazy=True)
    skills = db.relationship('Skill', backref='owner', lazy=True)
    projects = db.relationship('Project', backref='owner', lazy=True)
    certificates = db.relationship('Certificate', backref='owner', lazy=True)

class Internship(db.Model):

     id = db.Column(db.Integer, primary_key=True)
     company = db.Column(db.String(100), nullable=False)
     role = db.Column(db.String(100), nullable=False)
     start_date = db.Column(db.String(20), nullable=False)
     end_date = db.Column(db.String(20), nullable=True)
     notes = db.Column(db.Text, nullable=True)
     skills = db.Column(db.String(200), nullable=True)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    date_obtained = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


