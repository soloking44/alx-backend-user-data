#!/usr/bin/env python3
"""An auth class for user data testing
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> str:
    """Accepts in password text value
    outputs bytes (salted_hashed)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Outputs text of the new UUID
    apply uuid module
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to connect an authentication database
    """

    def __init__(self):
        """Sets up DB
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Accepts vital text (email, password) values
        outputs a user item
        issues valueError if exists
        User <user's email> already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Await email and password needed values
        outputs a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Accepts email text as value
        outputs the session ID as a text
        gets user matching email, create new UUID
        save in database as users session_id, output session ID
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Accepts single session_id text value
        Returns corresponding User or None
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Accepts a single user_id integer value
        outputs None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Accepts email value data, outputs the value
        gets user matching the email, issue valueError if not exist
        generate uuid and update users reset_token database field
        Return the token if exists
        """
        updated_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=updated_token)
            return updated_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> str:
        """Accept reset_token text value with password string
        outputs None
        apply reset_token to get matching user, issues valueError
        if it dont exist, if exist, hash password and modify user
        hashed_password data with new hashed password and reset_token
        data to None
        """
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
