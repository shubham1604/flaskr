import pytest
from flaskr.db import get_db
from flask import session, g


def test_register(client, app):

    assert client.get('/auth/register').status_code == 200
    response =  client.post('/auth/register', data = {'username':'a', 'password':'a'})
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
        "SELECT * from flaskr_user where username = ?",('a',)
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'),(
('', '', b'Username is not supplied'),
('','a',b'Username is not supplied'),
('a','', b'Password is not supplied'),
('test','test', b'Username is already taken')
))
def test_register_validate_input(client, username, password, message):

    response =  client.post(
    '/auth/register',
    data = {'username':username, 'password':password}
    )

    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'),(
('a','b', b"User is not registered"),
('test', 'test1', b'Incorrect Password'),
('test','',b'Please enter a password')
))
def test_validate_login(auth, username, password, message):
    response = auth.login(username = username, password = password)
    assert message in response.data

def test_logout(auth, client):

    auth.login()

    with client:
        # client.get('/')
        auth.logout()
        assert 'user_id' not in session
