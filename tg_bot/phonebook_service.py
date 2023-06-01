from tg_bot import db
from .models import PhonebookModel
from re import fullmatch


class PhonebookException(Exception):
    pass


class Phonebook:
    """
    This code defines a `Phonebook` class that provides methods for adding,
    getting and deleting contacts from a database.
    """

    @staticmethod
    def add_contact(name, phone_number, user_id):
        """
        This is a static method that adds a new contact to the phonebook database.
        :param name - the name of the contact
        :param phone_number - the phone number of the contact
        :param user_id - the user id of the contact
        :return None
        """
        new_contact = PhonebookModel(
            name=name,
            phone_number=phone_number,
            user_id=user_id
        )
        db.session.add(new_contact)
        db.session.commit()

    @staticmethod
    def get_contact(name, user_id):
        """
        This is a static method that retrieves contacts from the database based on a user's ID and a name search string. 
        :param name - the name search string
        :param user_id - the user ID
        :return a list of contacts that match the search criteria.
        """
        contacts = db.session.execute(
            db.select(PhonebookModel).where(
                PhonebookModel.user_id == user_id,
                PhonebookModel.name.like(f'%{name}%')
            )
        ).scalars().all()
        return contacts

    @staticmethod
    def get_one_contact(name, user_id):
        """
        This is a static method that retrieves a single contact from the phonebook database.
        :param name - the name of the contact to retrieve
        :param user_id - the id of the user who owns the contact
        :return The contact object from the database.
        """
        contact = db.session.execute(
            db.select(PhonebookModel).where(
                PhonebookModel.user_id == user_id,
                PhonebookModel.name.like(name)
            )
        ).scalar()
        return contact

    def delete_contact(self, name, user_id):
        """
        Deletes a contact from the database.
        :param self - the instance of the class
        :param name - the name of the contact to delete
        :param user_id - the id of the user who owns the contact
        :raises Exception if no matches are found
        :return None
        """
        contact = self.get_one_contact(name, user_id)
        if contact is None:
            raise Exception('No matches found.')
        else:
            db.session.delete(contact)
            db.session.commit()

    @staticmethod
    def validate_phone_number(phone_number):
        """
        This is a static method that validates a phone number.
        It uses a regular expression to check if the phone number is valid.
        :param phone_number - the phone number to validate
        :return True if the phone number is valid, False otherwise.
        """
        return fullmatch(r'(\+?\d\d\d|0)\d{9}$', phone_number)
