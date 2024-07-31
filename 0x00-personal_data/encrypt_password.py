#!/usr/bin/env python3
"""A script to secure passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Codes a password in a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Ensures the coded password is formed in the given password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
