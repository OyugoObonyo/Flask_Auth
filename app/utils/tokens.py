from app.models import BlacklistedToken
import datetime
import jwt
import os


def encode_auth_token(user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm='HS256'
        )

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        is_blacklisted = BlacklistedToken.is_blacklisted(auth_token)
        if is_blacklisted:
            return 'Session expired. Please log in again'
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        print('AUTH_TOKEN IS: ', auth_token)
        return 'Invalid token. Please log in again.'