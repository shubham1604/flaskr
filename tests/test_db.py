import pytest, sqlite3

from flaskr.db import get_db

def test_get_close_db(app):

    with app.app_context():
        conn = get_db()
        assert conn is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        conn.execute("SELECT 1")

    assert 'closed' in str(e)
