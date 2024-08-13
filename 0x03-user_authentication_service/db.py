#!/usr/bin/env python3
"""This DB Module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self):
        """Sets up a new DB object
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Hidden memoized session method (object)
        prevent used outside DB class
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Append new user in database
        outputs a user item
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Outpus initial row locate in users table
        as sorted by functions input values
        """
        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Apply find_user_by to find the user to modify
        modify user's data as send in functions value
        commit changes to database
        causes valueError if value does not match the user
        value send
        """
        user_to_update = self.find_user_by(id=user_id)
        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key, value in kwargs.items():
            if key in user_keys:
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()
