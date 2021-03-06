import pytest
from flaskr.db import get_db, db
from flaskr.models import Post


def test_index(client, auth):
    response = client.get('/')

    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()

    response = client.get('/')
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Edit" in response.data
    assert b"test title" in response.data

    assert b'by test on 2018-01-01' in response.data
    assert b'test body' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/delete/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(client, app, auth):

    with app.app_context():
        post = db.session.query(Post).filter(Post.id == 1).one_or_none()
        post.author_id = 2
        db.session.add(post)
        db.session.commit()

    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/delete/1').status_code == 403
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
'/3/update',
'/delete/4'
))
def test_exists_required(auth, client,path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create_required(client, auth, app):

    auth.login()
    response = client.get('/create')
    assert response.status_code == 200

    response = client.post('/create', data={'title': 'created', 'body': 'Some Content'})

    with app.app_context():
        # conn = get_db()
        count = db.session.query(Post).count()
        # count = conn.execute("SELECT COUNT(id) FROM flaskr_post").fetchone()[0]
        assert count == 2


def test_update(auth, client, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'body':'Some text', 'title':'Some title'})

    with app.app_context():

        post = db.session.query(Post).filter(Post.id == 1).one_or_none()
        assert post.body == 'Some text'


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/delete/1')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        post = db.session.query(Post).filter(Post.id == 1).one_or_none()
        assert post is None
