from flaskr.db import db


class User(db.Model):

    __tablename__ = "flaskr_users"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref="user", lazy=False)

    def __str__(self):
        return f"{self.username}"
