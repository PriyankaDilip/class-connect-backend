from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    comments = db.relationship('Comment', cascade='delete')

    #constructor
    def __init__(self, **kwargs):
        self.score = kwargs.get('score', 0)
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')

    #change class object into dictionary
    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'text': self.text,
            'username': self.username
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, **kwargs):
        self.score = kwargs.get('score', 0)
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')
        self.post_id = kwargs.get('post_id')

    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'text': self.text,
            'username': self.username
        }