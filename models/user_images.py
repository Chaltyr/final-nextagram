from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models.user import User


class User_img(BaseModel):
    # username = pw.CharField(unique=True)
    user_image = pw.CharField()
    user = pw.ForeignKeyField(User, backref="user_images")