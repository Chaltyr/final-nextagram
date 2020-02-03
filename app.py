import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import *
import braintree


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('MERCHANT_ID'),
        public_key=os.getenv('PUBLIC_KEY'),
        private_key=os.getenv('PRIVATE_KEY')
    )
)

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)




# braintree.dropin.create({
#   authorization: CLIENT_TOKEN_FROM_SERVER,
#   container: '#dropin-container'
# }, function (err, instance) {
#   /* ... */
# });

# @app.route("/client_token", methods=["GET"])
# def client_token():
#   return gateway.client_token.generate()


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
