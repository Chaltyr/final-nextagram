from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_img = pw.CharField(default = "82713262_2682749128428457_8666411295068651520_o.jpg")

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}"

        #  for create new user
        if self.id == None:
            if duplicate_username:
                self.errors.append("Username has already been taken!!!")
            if re.search(password_regex, self.password) == None:
                self.errors.append("Password needs to be 8 characters long with at least one letter and one number!!!!")
            else:
                self.password = generate_password_hash(self.password)

        #  for update user info
        else:

    # def validate_update(self):
    #     self.errors = []

            if self.username != self.new_name:
                username_is_taken = User.get_or_none(User.username == self.new_name)
                if username_is_taken != None:
                    self.errors.append('Username already taken!!!')
            
            if self.email != self.new_email:
                email_is_taken = User.get_or_none(User.email == self.new_email)
                if email_is_taken != None:
                    self.errors.append('Email already taken!!!')
            
            # if self.password != self.new_password:
                # password_is_taken = User.get_or_none(User.password == self.new_password)
                # if password_is_taken != None:
                    # self.errors.append('Password is the same!!!')
            if re.search(password_regex, self.new_password) == None:
                self.errors.append("Password needs to be 8 characters long with at least one letter and one number!!!!")
            else:
                self.username = self.new_name
                self.email = self.new_email
                # self.profile_img = self.new_profile_img
                self.password = generate_password_hash(self.new_password)

            
        # if self.name != self.new_name:
        #     username_is_taken = User.get_or_none(User.name == self.new_name)
        #     if username_is_taken != None:
        #         self.error.append('Username already taken!!!')
        
         


