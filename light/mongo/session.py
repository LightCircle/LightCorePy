from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict


# By default, Flask stores sessions on the client's side in cookies
# It uses cryptography to prevent them from tampering with session data
# However, it doesn't encrypt the data, so the user can see what's being stored
# In this example I will show you how to store the session in the database

# This is a session object. It is nothing more than a dict with some extra methods
class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


# Session interface is responsible for handling logic related to sessions
# i.e. storing, saving, etc
class MongoSessionInterface(SessionInterface):
    # Init connection
    def __init__(self, db=None, collection='sessions'):
        self.store = db[collection]

    def open_session(self, app, request):
        # Get session id from the cookie
        sid = request.cookies.get(app.session_cookie_name)

        # If id is given (session was created)
        if sid:
            # Try to load a session from mongodb
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                # Check if the session isn't expired
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_session['data'],
                                        sid=stored_session['sid'])

        # If there was no session or it was expired...
        # Generate a random id and create an empty session
        sid = str(uuid4())
        return MongoSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)

        # We're requested to delete the session
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        # Refresh the session expiration time
        # First, use get_expiration_time from SessionInterface
        # If it fails, add 1 hour to current time
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(hours=1)

        # Update the mongo document, where sid equals to session.sid
        self.store.update({'sid': session.sid},
                          {'sid': session.sid,
                           'data': session,
                           'expiration': expiration}, True)

        # Refresh the cookie
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True,
                            domain=domain)
