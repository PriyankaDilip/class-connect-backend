from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

classes = db.Table('courses',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.course_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)