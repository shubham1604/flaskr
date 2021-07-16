from flask import Flask, current_app
import os
from .db import db
from flask_migrate import Migrate
from flaskr import models
from flask_admin import Admin
from .admin import PostModelView, UserModelView


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://learning_user:learning_password@localhost:5432/learning_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        pass

    db.init_app(app)

    migrate = Migrate(app, db)
    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    app.config['FLASK_ADMIN_SWATCH'] = 'readable'
    admin = Admin(app, name='Microblog', template_mode='bootstrap3')
    admin.add_view(PostModelView(models.Post, db.session, name="All posts"))
    admin.add_view(UserModelView(models.User, db.session, name="All Users"))

    @app.route('/hello')
    def hello():
        return f"Hello World"

    return app
