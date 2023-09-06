# models/share.py

from datetime import datetime
from database import db

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    video = db.relationship('Video', backref='shares', lazy=True)
    user = db.relationship('User', backref='shares', lazy=True)

    def __repr__(self):
        return f'<Share {self.id}>'
