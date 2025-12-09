from datetime import datetime, timedelta
from db_init import User
import jwt


secret_key = "super_secret"
algoritm = "HS256"


def create_jwt(data, time):
    data.update({"exp": datetime.now() + timedelta(time)})
    return jwt.encode(data, secret_key, algoritm)


def access_jwt(token):
    data = jwt.decode(token, secret_key, algoritm)
    return User.get_or_none(id=data.id)
