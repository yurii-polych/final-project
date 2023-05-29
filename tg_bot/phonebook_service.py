from tg_bot import db
from .models import PhonebookModel
from re import fullmatch


class PhonebookException(Exception):
    pass


class Phonebook:

    @staticmethod
    def add_contact(name, phone_number, user_id):
        new_contact = PhonebookModel(
            name=name,
            phone_number=phone_number,
            user_id=user_id
        )
        db.session.add(new_contact)
        db.session.commit()

    @staticmethod
    def get_contact(name, user_id):
        contacts = db.session.execute(
            db.select(PhonebookModel).where(
                PhonebookModel.user_id == user_id,
                PhonebookModel.name.like(f'%{name}%')
            )
        ).scalars().all()
        return contacts

    @staticmethod
    def get_one_contact(name, user_id):
        contact = db.session.execute(
            db.select(PhonebookModel).where(
                PhonebookModel.user_id == user_id,
                PhonebookModel.name.like(name)
            )
        ).scalar()
        return contact

    def delete_contact(self, name, user_id):
        contact = self.get_one_contact(name, user_id)
        if contact:
            db.session.delete(contact)
            db.session.commit()
        else:
            return 'No contact matching that query was found in the phone book.'

    @staticmethod
    def validate_phone_number(phone_number):
        return fullmatch(r'(\+?\d\d\d|0)\d{9}$', phone_number)
