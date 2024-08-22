from ..models.user_models import User
from ..models.database import db
from ..aop.exceptions import *
from pymysql import IntegrityError



class UserRepository:
    def get_user_by_Id(self, userId):
        return db.query(User).get(userId)

    def add_user(self, new_user):
        db.add(new_user)
        try:
            db.commit()
            user_id = self.get_user_by_email(new_user.email).userId
            return True, "User registered successfully.", user_id
        except IntegrityError as e:
            db.rollback()
            return False, str(e), None

    def get_user_by_email(self, email):
        return db.query(User).filter_by(email=email).first()

    def get_email_by_user(self, user_id):
        return self.get_user_by_Id(user_id).email

    def authenticate_user(self, email, password):
        this_user = self.get_user_by_email(email)
        print("this_user email: ", this_user.email)
        print("this_user password: ", this_user.password)
        print("input password: ", password)
        if password == this_user.password:
            return this_user.userId, this_user.type
        else:
            return None, None