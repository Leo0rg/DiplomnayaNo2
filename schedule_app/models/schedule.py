from . import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    teacher = db.relationship('User', backref='schedules') 