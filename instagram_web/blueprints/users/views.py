from flask import Blueprint, render_template, flash, redirect, request, abort, session, url_for
from models.user import User
from models.user_images import User_img
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# users#new - show sign up form
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# users#create for form action
@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("user_name")
    email = request.form.get("user_email")
    password = request.form.get("user_password")
    
    create_user = User(username = username, email = email, password = password)
    if create_user.save():
        login_user(create_user)
        flash(f"User {username} has been created!!!")
        return redirect('/')
    else:
        flash(f"Error has occured")
        return render_template("users/new.html", username = username)  
        
# users#show - show one user
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username==username)
    images = User_img.select().where(User_img.user==user.id)
    return render_template("users/user_profile.html", images=images,user=user,aws_domain=os.getenv('AWS_DOMAIN'))
    abort(404)


# users#index - list all users
@users_blueprint.route('/', methods=["GET"])
def index():
    user = User.select()
    return render_template('users/home.html', users=user)

# users#edit - show user edit page
@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit.html', errors=['error1', 'error2'])

# users#update for form action
@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    new_username = request.form.get('user_name')
    new_email = request.form.get('user_email')
    new_password = request.form.get('new_password')
    new_password_confirmation = request.form.get('new_password_confirmation')
    # new_profile_img = request.form.get('new_profile_img')

    if new_password == new_password_confirmation:

        user = User.get_by_id(current_user.id)
        user.new_name = new_username
        user.new_email = new_email
        user.new_password = new_password    
        # user.new_profile_img = new_profile_img

        # user.validate_update()

        if user.save():
            # User.update(username = new_username, email = new_email).where(User.id == current_user.id).execute()
            flash('Success!!!')
            return redirect (url_for('home'))

        else:
            flash(user.errors)
            return render_template('users/edit.html', errors=user.errors)

@users_blueprint.route('/edit_img', methods=['GET'])
def edit_img():
    return render_template('users/edit.html')

@users_blueprint.route('/img_update', methods=['POST'])
def img_update():
    if 'new_profile_img' not in request.files:
        flash('No image_file key in request.files')
        return redirect(url_for('users.edit_img'))

    file = request.files['new_profile_img']

    if file.filename == '':
        flash('No file was selected')
        return redirect(url_for('users.edit_img'))
    
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)
        if output:
            User.update(profile_img = output).where(User.id==current_user.id).execute()
            flash('Upload success')
            return redirect(url_for('home'))
        else:
            flash('Unable to upload, try again')
            return redirect('edit_img')
    else:
        flash('File type not supported!!!')
        return redirect(url_for('edit_img'))



@users_blueprint.route('/upload', methods=['GET'])
def upload():
    return render_template('users/img_upload.html')

@users_blueprint.route('/img_upload', methods=['POST'])
def img_upload():
    if 'user_img' not in request.files:
        flash('No image_file key in request.files')
        return redirect(url_for('users.img_upload'))

    file = request.files['user_img']

    if file.filename == '':
        flash('No file was selected')
        return redirect(url_for('users.img_upload'))
    
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)
        if output:
            User_img(user=current_user.id, user_image=output).save()
            # User.update(profile_img = output).where(User.id==current_user.id).execute()
            flash('Upload success')
            return redirect(url_for('users.show', username=current_user.username))
        else:
            flash('Unable to upload, try again')
            return redirect('upload')
    else:
        flash('File type not supported!!!')
        return redirect(url_for('upload'))


    