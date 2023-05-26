from tg_bot import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(30))
    last_message = db.Column(db.String(255), default=False)
    created = db.Column(db.DateTime, default=datetime.now())


