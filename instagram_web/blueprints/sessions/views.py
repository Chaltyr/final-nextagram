from flask import Flask, Blueprint, session, render_template, flash, url_for, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user
from models.user import *
from app import app
from werkzeug.security import check_password_hash
from instagram_web.helpers.google_oauth import oauth
# from models.user import *

login_manager = LoginManager()
login_manager.init_app(app)

sessions_blueprint = Blueprint('sessions', __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@sessions_blueprint.route('/', methods=['GET'])
def index():
    return "SESSIONS"

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html') #WHY DOES THIS NOT NEED ('sessions/new.html')???

@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.username==request.form.get('user_name'))
    if user:
        password = request.form.get('user_password')
        hashed_password = user.password
        result = check_password_hash(hashed_password, password)
        if result:
            login_user(user)
            flash("success login!","danger")
            return redirect(url_for("users.index"))
        else:
            flash("cannot login!", "danger")
            return redirect(url_for("sessions.new"))
    else:
        flash("user not exist!", "danger")
        return render_template("users/new.html")


@sessions_blueprint.route('/delete')
@login_required
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/google', methods=['GET'])
def google():
    redirect_uri = url_for('sessions.authorize',_external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize')
# @login_required
def authorize():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    info = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
    print(info)
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)

        flash(f'Google email: {email} login success!!!!!!!!!')
        return redirect(url_for('users.show', username=user.username))
    else:
        flash(f'{email} is not registered!!!')
        return redirect(url_for('sessions.new'))