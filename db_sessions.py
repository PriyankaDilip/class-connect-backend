# from old users_dao
"""
def renew_session(update_token):
    user = get_user_by_update_token(update_token)

    if user is None:
        raise Exception('Invalid update token.')

    user.renew_session()
    db.session.commit()
    return user
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    token = #???
    refresh = #???

    def __init__(self, **kwargs):                                                   self.user_id = kwargs.get('user_id')
        self.token = kwargs.get('token')
        self.refresh = kwargs.get('refresh')

        self.renew_session()

    def serialize(self):
        return {
            'session_id' = self.session_id,
            'user_id': self.user_id
        }