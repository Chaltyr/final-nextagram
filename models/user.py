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

    def follow(self, user):
        from models.follow import Follow
        if self.id != user.id and self.is_following(user) == False and self.is_requesting(user) == False:
            follow = Follow(follower_id=self.id, followed_id=user.id)
            follow.save()
        else:
            return 0

    def approve(self, user):
        from models.follow import Follow
        if user.is_requesting(self):
            Follow.update(approve=True).where(Follow.followed_id == self.id, Follow.follower_id == user.id).execute()
        else:
            return 0

    def get_requests(self):
        from models.follow import Follow
        result = User.select().join(Follow, on=(follower_id==User.id).where(Follow.followed_id==self.id, Follow.approved==False))
        return result

    def get_follower(self):
        from models.follow import Follow
        result = User.select().join(Follow, on=(follower_id==User.id).where(Follow.followed_id==self.id, Follow.approved==True))
        return result

    def get_requesting(self):
        from models.follow import Follow
        result = User.select().join(Follow, on=(followed_id==User.id).where(Follow.follower_id==self.id, Follow.approved==False))
        return result

    def get_following(self):
        from models.follow import Follow
        result = User.select().join(Follow, on=(followed_id==User.id).where(Follow.follower_id==self.id, Follow.approved==True))
        return result

    def is_following(self, user):
        from models.follow import Follow
        result = Follow.select().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved== True)
        if len(result) > 0:
            return True
        else:
            return False

    def is_requesting(self, user):
        from models.follow import Follow
        result = Follow.select().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved== False)
        if len(result) > 0:
            return True
        else:
            return False

    def unfollow(self, user):
        from models.follow import Follow
        if self.is_following(user):
            Follow.delete().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == True).execute()
        else:
            return 0
    
    def cancel_request(self, user):
        from models.follow import Follow
        if self.is_requesting(user):
            Follow.delete().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == False).execute()
        else:
            return 0
    
    def reject(self, user):
        from models.follow import Follow
        if user.is_requesting(self):
            Follow.delete().where(Follow.followed_id == self.id, Follow.follower_id == user.id, Follow.approved == False).execute()
        else:
            return 0

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
        
         

