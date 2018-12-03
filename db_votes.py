from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cand(db.Model):
    __tablename__ = 'courses'
    cand_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    expert_name  = db.Column(db.String, nullable=False)
    expert_type = db.Column(db.String, nullable=False)
    days = db.Column(db.String(7), nullable=False) # MTWRFAU
    time = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.expert_name = kwargs.get('expert_name', "")
        self.expert_type = kwargs.get('expert_type', 'TA')
        self.days = kwargs.get('days', "1,0,0,0,0,0,0")
        self.time = kwargs.get('time', "09:00-13:00")

        self.renew_session()

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
            'title': self.title,
            'expert_name': self.expert_name,
            'expert_type': self.expert_type,
            'days': string_to_days(self.days),
            'time': self.time
        }