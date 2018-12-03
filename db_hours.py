from flask_sqlalchemy import SQLAlchemy
#import datetime
import db_course

db = SQLAlchemy()

class Hours(db.Model):
    __tablename__ = 'hours'
    oh_id = db.Column(db.Integer, primary_key=True)
    expert_name  = db.Column(db.String, nullable=False) # name of prof or TA
    expert_type = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False) 
    end_time = db.Column(db.String, nullable=False)
    days = db.Column(db.String(7), nullable=False) # MTWRFAU
    location = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

    def __init__(self, **kwargs):
        self.expert_name = kwargs.get('expert_name')
        self.expert_type = kwargs.get('expert_type', "TA")
        self.start_time = kwargs.get('start_time', "09:00") 
        #datetime.datetime.now().time
        self.end_time = kwargs.get('end_time', "13:00")

        #self.start_time + datetime.timedelta(hours=1)
        self.days = kwargs.get('days', "1,0,0,0,0,0,0")
        course_id = kwargs.get('course_id')
        location = kwargs.get('location')

    def string_to_days(str):
        x = str.split(",")
        days_json = {}
        counter=0
        flag = true
        for i in range(0, 7):
            if x[counter] == "1":
                flag=true
            else:
                flag=false

            if counter==0: 
                days_json["Monday"] = flag
            elif counter==1:
                days_json["Tuesday"] = flag
            elif counter==2:
                days_json["Wednesday"] = flag
            elif counter==3:
                days_json["Thursday"] = flag
            elif counter==4:
                days_json["Friday"] = flag
            elif counter==5:
                days_json["Saturday"] = flag
            else:
                days_json["Sunday"] = flag

            counter = counter+1

        return json.dumps(days_json)

    def serialize(self):
        return {
            'oh_id': self.oh_id,
            'expert_name': self.expert_name,
            'expert_type': self.expert_type,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'days' : string_to_days(self.days),
            'location': self.location
        }