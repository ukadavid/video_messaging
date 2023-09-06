# models/user.py

from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    videos = db.relationship('Video', backref='user', lazy=True)
    shares = db.relationship('Share', backref='user', lazy=True)
