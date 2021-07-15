from flaskr.db import db
from datetime import datetime


class Post(db.Model):

    __tablename__ = "flaskr_posts"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("flaskr_users.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
