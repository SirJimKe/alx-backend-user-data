#!/usr/bin/env python3
"""SessionDBAuth module"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """Session Authentication with Database Storage"""

    def create_session(self, user_id=None):
        """Creates a Session ID and stores in the database"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user ID based on a session ID from the database"""
        if session_id is None:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
