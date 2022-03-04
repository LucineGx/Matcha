import functools

from flask import (
    Blueprint, current_app, g, redirect, request, session, url_for, render_template
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
import secrets

from flaskr.db import get_db
from .db_utils.user_model import user as user_model
from .db_utils.sql_wrapper import create_single_instance, update_user, get_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', ))
def register():
    db = get_db()
    error = None
    status = 500

    new = dict(request.form)

    # To do: add more constraints and checks !
    for field, spec in user_model["fields"].items():
        if spec["required"] is True:
            if field not in new or new[field] is None:
                error = f"{field} is required"
                status = 400

    if error is None:
        new["confirmation_token"] = secrets.token_urlsafe(20)
        try:
            create_single_instance(db, "user", new, user_model["fields"])
        except db.IntegrityError:
            error = f"{new['email']} is already registered"
            status = 409
        else:
            send_confirmation_mail(new)
            return f"User {new['email']} successfully saved", 201

    return error, status


def send_confirmation_mail(new_user: dict):
    mail = Mail(current_app)
    subject = "Confirm your email"
    confirm_url = url_for("auth.confirm_register", token=new_user["confirmation_token"], _external=True)
    html = render_template(
        'confirmation_mail.html',
        user_name=new_user["firstname"],
        confirm_url=confirm_url)
    msg = Message(html=html, subject=subject, recipients=[new_user["email"]])
    mail.send(msg)


@bp.route('/register/confirm/<token>', methods=('GET',))
def confirm_register(token):
    user = get_user("confirmation_token", token)

    if user is None:
        error = "Unknown token."
        status = 404
    elif user["confirmed"]:
        error = "This user has already confirmed his email."
        status = 409
    else:
        update_user(update={"confirmation_token": None, "confirmed": True}, conditions={"id": user["id"]})
        return "User confirmed successfully", 200

    return error, status


@bp.route('/login', methods=('POST',))
def login():
    user = get_user("email", request.form["email"])

    if user is None:
        error = 'Incorrect email or password'
        status = 401
    elif not check_password_hash(user['password'], request.form["password"]):
        error = 'Incorrect email or password'
        status = 401
    elif not user["confirmed"]:
        error = "User email is not confirmed"
        status = 401
    else:
        session.clear()
        session['user_id'] = user['id']
        return "Login successful", 200

    return error, status


@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return "Logout successful", 200


@bp.route('/forgot-password', methods=('POST',))
def forgot_password():
    response_message = "If a user is linked to this mail address, a link has been send to reinitialize the password."
    user = get_user("email", request.form["email"])

    if user is not None:
        token = secrets.token_urlsafe(20)
        update_user(update={"password_reinit_token": token}, conditions={"id": user["id"]})

        mail = Mail(current_app)
        subject = "Reinitialize your password"
        url = f"http://localhost:3000/auth/change_password/{token}"
        html = render_template(
            'forgot_password.html',
            user_name=user["firstname"],
            url=url)
        msg = Message(html=html, subject=subject, recipients=[user["email"]])
        mail.send(msg)

    return response_message, 200


@bp.update_password('/update-password/<token>', methods('POST',))
def update_password():
    user = get_user("confirmation_token", token)

    if user is None:
        error = "Unknown token."
        status = 404
    else:
        update_user(update={"confirmation_token": None, "password": request.form["password"]}, conditions={"id": user["id"]})
        return "User confirmed successfully", 200

    return error, status


@bp.before_app_request
def load_logged_in_user():
    """
    To do: check this is used
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
