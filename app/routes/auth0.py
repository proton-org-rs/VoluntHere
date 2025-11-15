from flask import Blueprint, redirect, url_for, current_app, request, session
from flask_login import login_user, logout_user
from app import db
from app.models import User
from urllib.parse import urlencode
import os

auth0_bp = Blueprint("auth0", __name__)

@auth0_bp.route("/login")
def login():
    return current_app.auth0.authorize_redirect(
        redirect_uri=os.getenv("AUTH0_CALLBACK_URL"),
        audience=os.getenv("AUTH0_AUDIENCE")
    )

def generate_unique_username(base_username):
    from app.models import User

    username = base_username
    counter = 1

    # Dok postoji korisnik sa istim usernameom – dodaj suffiks
    while User.query.filter_by(username=username).first():
        username = f"{base_username}{counter}"
        counter += 1

    return username


@auth0_bp.route("/callback")
def callback():
    token = current_app.auth0.authorize_access_token()
    userinfo = token.get("userinfo")

    if not userinfo:
        return "Auth0 returned no user info", 400

    email = userinfo.get("email") or f"{userinfo['sub'].replace('|', '_')}@auth0.local"

    raw_username = userinfo.get("nickname") or email.split("@")[0]
    username = generate_unique_username(raw_username)

    name = userinfo.get("name", username)
    avatar = userinfo.get("picture")

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=username,
            name=name,
            email=email,
            password_hash="AUTH0_USER",
            role="user",
            profile_pic=avatar
        )
        db.session.add(user)
    else:
        if not user.profile_pic and avatar:
            user.profile_pic = avatar

    db.session.commit()
    login_user(user)

    return redirect(url_for("main.index"))


@auth0_bp.route("/logout")
def logout():
    logout_user()

    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")

    return redirect(
        f"https://{domain}/v2/logout?"
        f"client_id={client_id}&"
        f"returnTo={url_for('main.index', _external=True)}"
    )

