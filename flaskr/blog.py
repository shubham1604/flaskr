from flask import Blueprint, render_template, request, g, redirect, url_for, abort, flash
from .db import get_db, db
from .auth import login_required
from flaskr.models import User, Post
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = db.session.query(Post).join(User).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is not there"

        if error is None:

            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)

    return render_template("blog/create.html")


def get_post(id, check_author=True):

    post = db.session.query(Post).filter(Post.id == id).one_or_none()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    post = get_post(id)
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is not there"

        if error is None:

            post = db.session.query(Post).filter(Post.id == id).one_or_none()
            post.title = title
            post.body = body

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)
    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):

    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
