from flask import Blueprint, render_template, flash, redirect, request, abort, session, url_for
from models.user import User
from models.user_images import User_img
from models.endorsements import Endorsement
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
import os
from app import gateway
from instagram_web.util.mail_helper import mail

endorsements_blueprint = Blueprint('endorsements',
                                     __name__, 
                                     template_folder="templates")

@endorsements_blueprint.route('/new/<id>', methods=["GET"])
def index(id):
    print(id)
    client_token = gateway.client_token.generate()
    return render_template('endorsements/new.html',client_token=client_token, id=id)


@endorsements_blueprint.route('/<id>', methods=["POST"])
def create(id): 
    nonce = request.form.get('nonce')
    amount = request.form.get('amount')
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
        "submit_for_settlement": True
        }
    })
    endorse = Endorsement(amount=amount, image=id, user=current_user.id)
    endorse.save()
    mail(current_user)
    flash (f'Payment send, thank you for your support!!!')
    return redirect (url_for('users.show',username=current_user.username))