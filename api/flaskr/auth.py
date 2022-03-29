from flask import (
    Blueprint, current_app, g, request, session, url_for, render_template
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
import secrets

from flaskr.db import get_db
from flaskr.user import update_user, get_user, validate_user, create_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', ))
def register():
    status = 500

    new_user = dict(request.form)
    error = validate_user(new_user)
    if error:
        status = 400

    if error is None:
        db = get_db()
        try:
            create_user(new_user, db)
        except db.IntegrityError:
            error = f"{new_user['email']} is already registered"
            status = 409
        else:
            send_confirmation_mail(get_user("email", new_user["email"]))
            return f"User {new_user['email']} successfully saved", 201

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
def confirm_register(token: str):
    user = get_user("confirmation_token", token)

    if user is None:
        return "Unknown token.", 404

    else:
        update_user(
            update={"confirmation_token": None, "confirmed": True},
            conditions={"id": user["id"]},
            should_format_values=False
        )
        return "User confirmed successfully", 200


@bp.route('/login', methods=('POST',))
def login():
    user = get_user("email", request.form["email"])

    if user is None:
        return 'Incorrect email or password', 401

    elif not check_password_hash(user['password'], request.form["password"]):
        return 'Incorrect email or password', 401

    elif not user["confirmed"]:
        return "User email is not confirmed", 401

    else:
        session.clear()
        session['user_id'] = user['id']
        return "Login successful", 200


@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return "Logout successful", 200


@bp.route('/forgot-password', methods=('POST',))
def forgot_password():
    response_message = "If a user is linked to this mail address, a link has been send to reinitialize the password"
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


@bp.route('/update-password/<token>', methods=('POST',))
def update_password(token: str):
    user = get_user("password_reinit_token", token)

    if user is None:
        return "Unknown token", 404
    else:
        update_user(update={"password_reinit_token": None, "password": request.form["password"]}, conditions={"id": user["id"]})
        return "Password updated successfully", 200


@bp.before_app_request
def load_logged_in_user():
    """
    To do: check this is used
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_user("id", user_id)
