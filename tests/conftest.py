import pytest , tempfile, os
from flaskr import create_app
from flaskr.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as fh:
    _sql_command = fh.read().decode('utf-8')
    print()

@pytest.fixture
def app():
    fh_db, db_path = tempfile.mkstemp()
    app = create_app({'TESTING':True,'DATABASE':db_path})

    with app.app_context():
        init_db()
        get_db().executescript(_sql_command)

    yield app

    os.close(fh_db)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner():
    return app.test_cli_runner()

class AuthAction(object):

    def __init__(self, client):
        self._client = client

    def login(self, username = 'test', password = 'test'):
        return self._client.post('/auth/login',data = {'username':username, 'password':password })

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthAction(client)
