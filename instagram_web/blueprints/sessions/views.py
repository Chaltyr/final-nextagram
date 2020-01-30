from flask import Flask, Blueprint, session, render_template, flash, url_for, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user
from models.user import *
from app import app
from werkzeug.security import check_password_hash
from models.user import *

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