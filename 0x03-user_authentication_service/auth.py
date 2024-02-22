"""Hashed password"""
#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """Generate a salted hash of the input password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password