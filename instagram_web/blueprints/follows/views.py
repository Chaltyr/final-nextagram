from flask import Blueprint, render_template, flash, redirect, request, abort, session, url_for
from models.user import User
from models.user_images import User_img
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
import os
from models.follow import Follow


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/follow/<id>', methods=['GET'])
@login_required
def follow(id):
    user = User.get_by_id(id)
    current_user.follow(user)
    return redirect(url_for('home'))

@follows_blueprint.route('/cancel/<id>', methods=['GET'])
@login_required
def cancel(id):
    user = User.get_by_id(id)
    current_user.cancel_request(user)
    return redirect(url_for('home'))

@follows_blueprint.route('/unfollow/<id>', methods=['GET'])
@login_required
def unfollow(id):
    user = User.get_by_id(id)
    current_user.unfollow(user)
    return redirect(url_for('home'))

@follows_blueprint.route('/show/<id>', methods=['GET'])
@login_required
def show(id):
    user = User.get_by_id(id)
    # current_user.approve(user)
    return render_template('follows/show.html')

@follows_blueprint.route('/approve/<id>', methods=['GET'])
@login_required
def approve(id):
    user = User.get_by_id(id)
    current_user.approve(user)
    return redirect(url_for('home'))



