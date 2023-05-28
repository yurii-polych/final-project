from tg_bot import db
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(30))
    last_message = db.Column(db.String(255), default=False)
    created = db.Column(db.DateTime, default=datetime.now())


class PhonebookModel(db.Model):
    __tablename__ = 'phonebook'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint('name', 'user_id', name='unique_name_phone_number'),)
