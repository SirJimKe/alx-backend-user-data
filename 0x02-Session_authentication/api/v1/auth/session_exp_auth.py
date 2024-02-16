#!/usr/bin/env python3
"""SessionExpAuth module"""

from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv

class SessionExpAuth(SessionAuth):
    """Session Authentication with Expiration"""

    def __init__(self):
        """Initialize SessionExpAuth"""
        super().__init__()
        session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a Session ID with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user ID based on a session ID with expiration"""
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data.get("user_id")
        created_at = session_data.get("created_at")
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session_data.get("user_id")
