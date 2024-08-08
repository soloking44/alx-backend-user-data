#!/usr/bin/env python3
"""
Method of user_session
"""
from models.base import Base


class UserSession(Base):
    """
    A class that represent user session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize UserSession object
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
