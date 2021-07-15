from flask import Blueprint, flash, request, render_template, redirect, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import db, get_db
import functools
from flaskr.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET','POST'))
def register():

    # import pdb;pdb.set_trace()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        # db = get_db()
        if not username:
            error = "Username is not supplied"
        elif not password:
            error = "Password is not supplied"
        elif db.session.query(User.username).filter(User.username == username).first():
            error = "This Username is already taken"

        if not error:
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # db.execute("insert into flaskr_user(username, password) values(?,?)",(username, generate_password_hash(password)))
            # db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=("GET", "POST"))
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # db = get_db()
        # user = db.execute('Select * from flaskr_user where username = ?', (username,)).fetchone()
        user = db.session.query(User).filter(User.username == username).one_or_none()
        error = None
        if user is None:
            error = "User is not registered"
        elif not password:
            error = "Please enter a password"
        elif not check_password_hash(user.password, password):
            error = "Incorrect Password"

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_loggedin_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).one_or_none()
        # g.user = get_db().execute("SELECT * from flaskr_user where id = ?",(user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return view(*args, **kwargs)

    return wrapped_view
