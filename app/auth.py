import os
from flask import Blueprint, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from dotenv import load_dotenv

load_dotenv()
auth_bp = Blueprint("auth", __name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

google_bp = make_google_blueprint(client_id=os.getenv("GOOGLE_CLIENT_ID"),
                                  client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                                  redirect_to="auth.google_auth_callback",
                                   scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"])
auth_bp.register_blueprint(google_bp, url_prefix="/login")

@auth_bp.route("/google_auth_callback")
def google_auth_callback():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()

    user = User.query.filter_by(google_id=user_info["id"]).first()
    if not user:
        user = User(google_id=user_info["id"],
                    name=user_info["name"],
                    email=user_info["email"],
                    profile_pic=user_info.get("picture"))
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for("auth.dashboard"))

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return f"Hello, {current_user.name}! <a href='/logout'>Logout</a>"

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
