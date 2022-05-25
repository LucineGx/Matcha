from flask import (
    Blueprint, current_app, g, request, session, url_for, render_template
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
import secrets

from flaskr.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', ))
def register():
    msg, status_code = User.create(request.form)

    if status_code == 201:
        token = secrets.token_urlsafe(20)
        User.update(
            {"confirmation_token": token, "confirmed": 1},
            {"email": request.form["email"]}
        )
        #send_confirmation_mail(request.form, token)
        msg = "User created successfully"

    return msg, status_code


def send_confirmation_mail(new_user: dict, token: str):
    mail = Mail(current_app)
    subject = "Confirm your email"
    confirm_url = url_for("auth.confirm_register", token=token, _external=True)
    html = render_template(
        'confirmation_mail.html',
        user_name=new_user["first_name"],
        confirm_url=confirm_url)
    msg = Message(html=html, subject=subject, recipients=[new_user["email"]])
    mail.send(msg)


@bp.route('/register/confirm/<token>', methods=('GET',))
def confirm_register(token: str):
    user = User.get("confirmation_token", token)

    if user is None:
        return "Unknown token", 404

    else:
        User.update(
            form={"confirmation_token": None, "confirmed": 1},
            conditions={"id": user["id"]},
        )
        return "User confirmed successfully", 200


@bp.route('/login', methods=('POST',))
def login():
    user = User.get("email", request.form["email"]).fetchone()

    if user is None:
        return 'Incorrect email or password', 401

    elif not check_password_hash(user['password'], request.form["password"]):
        return 'Incorrect email or password', 401

    elif not user["confirmed"]:
        return "User email is not confirmed", 401

    else:
        session.clear()
        session['user_id'] = user['id']
        return User._expose(user, 200)


@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return "Logout successful", 200


@bp.route('/forgot-password', methods=('POST',))
def forgot_password():
    response_message = "If a user is linked to this mail address, a link has been send to reinitialize the password"
    user = User.get("email", request.form["email"])

    if user is not None:
        token = secrets.token_urlsafe(20)
        User.update(
            form={"password_reinit_token": token},
            conditions={"id": user["id"]}
        )

        mail = Mail(current_app)
        subject = "Reinitialize your password"
        url = f"http://localhost:3000/auth/change_password/{token}"
        html = render_template(
            'forgot_password.html',
            user_name=user["first_name"],
            url=url)
        msg = Message(html=html, subject=subject, recipients=[user["email"]])
        mail.send(msg)

    return response_message, 200


@bp.route('/update-password/<token>', methods=('POST',))
def update_password(token: str):
    user = User.get("password_reinit_token", token)

    if user is None:
        return "Unknown token", 404
    else:
        msg, status_code = User.safe_update(
            form={"password_reinit_token": None, "password": request.form["password"]},
            on_col="id",
            for_val=user["id"]
        )
        if status_code == 201:
            msg = "Password updated successfully"
        return msg, status_code


@bp.before_app_request
def load_logged_in_user():
    """
    To do: check this is used
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get("id", user_id)
