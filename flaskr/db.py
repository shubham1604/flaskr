from flask import g, current_app
import sqlite3
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():

    conn = get_db()
    with current_app.open_resource('schema.sql') as fh:
        conn.executescript(fh.read().decode('utf8'))


def get_db():
    pass

    if 'db' not in g:
        # create connection
        # g.db = connection
        g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types = sqlite3.PARSE_DECLTYPES)

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialised the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
