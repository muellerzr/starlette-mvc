import sqlalchemy
import bcrypt
import jwt
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
import configs


def create_users_table(metadata):
    return sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("hashed", sqlalchemy.LargeBinary),
    )


# for user authentication
class userAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        jwt_cookie = request.cookies.get('jwt')
        if jwt_cookie:      # cookie exists
            try:
                payload = jwt.decode(jwt_cookie.encode('utf8'), str(configs.SECRET_KEY), algorithms=['HS256'])
                return AuthCredentials(["user_auth"]), SimpleUser(payload['username'])
            except:
                raise AuthenticationError('Invalid auth credentials')
        else: 
            return      # unauthenticated

def get_hashed_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password:str, hashed_pass):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass)

def generate_jwt(username):
    payload = {'username': username}
    token = jwt.encode(payload, str(configs.SECRET_KEY), algorithm='HS256').decode('utf-8')
    return token
