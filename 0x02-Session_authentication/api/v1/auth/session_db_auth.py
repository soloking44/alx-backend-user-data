#!/usr/bin/env python3
"""
Module session_db_auth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime


class SessionDBAuth(SessionExpAuth):
    """
    A class that represent database for session authentication
    """
    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id with expire time

        Parameters
        ----------
        user_id: str
            user id

        Returns
        -------
        str
          A session id for user id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return
        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Reterive a User ID based on a Session ID from database:

        Parameters
        ---------
        session_id: str
          A session id

        Returns
        -------
        str
            A user id
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None

        user_session = user_session[0]

        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Deletes the user session / logout

        Parameters
        ----------
        request: object
            request object found when http request is sent

        Returns
        -------
        bool
            True if the session id is deleted associate with
            the user otherwise False
        """
        if request is None:
            return
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
        except Exception:
            return False

        return True
