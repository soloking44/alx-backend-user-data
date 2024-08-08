#!/usr/bin/env python3
"""
Handle api authentication setup
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """
    Handle api authentication process
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Output boolean """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']

        for stars in astericks:
            if path.startswith(stars):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Output Flask item """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Flask request item """
        return None

    def session_cookie(self, request=None):
        """ Outputs request cookie value """
        if request is None:
            return None
        cookie = getenv('SESSION_NAME')
        return request.cookies.get(cookie)
