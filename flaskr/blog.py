from flask import Blueprint, render_template, request, g, redirect, url_for, abort, flash
from .db import get_db
from .auth import login_required
bp = Blueprint('blog',__name__)



@bp.route('/')
def index():

    conn = get_db()
    posts = conn.execute("SELECT * FROM  flaskr_post p join flaskr_user u on p.author_id = u.id order by created desc").fetchall()

    return render_template('blog/index.html', posts = posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is not there"

        if error is None:

            db = get_db()
            db.execute("INSERT INTO flaskr_post(title, body, author_id) values (?,?,?)", (title, body, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)

    return render_template("blog/create.html")


def get_post(id, check_author = True):

    post = get_db().execute("SELECT * from flaskr_post where id = ?", (id,)).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
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

            db = get_db()
            db.execute("UPDATE flaskr_post set title = ?, body = ? where id = ?", (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))
        else:
            flash(error)
    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:id>',methods = ['POST'])
@login_required
def delete(id):

    post = get_post(id)
    conn = get_db()
    conn.execute("DELETE from flaskr_post where id = ?", (id,))
    conn.commit()
    return redirect(url_for('blog.index'))
