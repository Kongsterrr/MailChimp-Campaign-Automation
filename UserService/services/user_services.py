from ..models.user_models import User
from ..repos.user_repos import UserRepository
from ..aop.exceptions import *
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()  # it's better to use dependency injection here

    def get_user(self, userId):
        User = self.user_repository.get_user_by_Id(userId)
        if User is None:
            raise ('User not found')
        return User

    def authenticate_user(self, user_email, password):
        return self.user_repository.authenticate_user(user_email, password)

    def create_user(self, user_data):
        try:
            new_user = User(**user_data)
            success, message, user_id = self.user_repository.add_user(new_user)
            return success, message, user_id
        except IntegrityError as e:
            return False, str("This email is already registered."), None
        except Exception as e:
            raise