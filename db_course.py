from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    subject  = db.Column(db.String(5), nullable=False) # "PUNJB"
    catalogNbr = db.Column(db.String, nullable=False) # "2110"
    title = db.Column(db.String, nullable=False)
    hours = db.relationship('Hours', cascade='delete')

    def __init__(self, **kwargs):  
        self.subject = kwargs.get('subject')
        self.catalogNbr = kwargs.get('catalogNbr')
        self.title = kwargs.get('title', '')

        self.renew_session()

    def serialize(self):
        return {
            'course_id': self.course_id,
            'subject': self.subject,
            'catalogNbr': self.catalogNbr,
            'title': self.title
        }