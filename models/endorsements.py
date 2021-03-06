from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models.user import User
from models.user_images import User_img
from models.follow import Follow


class Endorsement(BaseModel):
    amount = pw.CharField()
    image = pw.ForeignKeyField(User_img, backref="endorsements")
    user = pw.ForeignKeyField(User, backref="endorsements")
