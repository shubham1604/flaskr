import pytest
import tempfile
import json
from datetime import datetime
import os
from flaskr import create_app
from flaskr.models import User, Post
from flaskr.db import db

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")


def create_db_tables():
    db.create_all()


def populate_db():

    users = os.path.join(TEST_DIR, "user.json")
    with open(users) as inf:
        users = json.load(inf)
    [db.session.add(User(**user)) for user in users]
    db.session.commit()

    posts = os.path.join(TEST_DIR, "post.json")
    with open(posts) as infl:
        posts = json.load(infl)

    for post in posts:
        date_time = post.get('created', None)
        post.update({
            'created': datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        })
        db.session.add(Post(**post))

    db.session.commit()


def drop_db_tables():
    db.drop_all()


def truncate_db():
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()


@pytest.fixture
def app():
    fh_db, db_path = tempfile.mkstemp()

    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path})
    # app = create_app({'TESTING': True})
    with app.app_context() as ctx:
        drop_db_tables()   # drop any existing tables (in case the exist) from previous test
        create_db_tables()
        populate_db()
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

    def login(self, username='test', password='test'):
        return self._client.post('/auth/login',data = {'username': username, 'password': password })

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthAction(client)
