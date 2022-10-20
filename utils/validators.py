import re
from email_validator import validate_email

# Username should be at least 3 characters long
# and can contain any char between 0-9, a-z or A-Z
# non-alphanumeric characters allowed on username are (. or _ or -)
USERNAME_REGEX = re.compile(r"\A[\w\-\.]{3,}\Z")
# Password should be at least 6 characters long
# must contain at least 1 upperase, one lowercase and 1 digit
# password can also contain a special character
PASSWORD_REGEX = re.compile(r"\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z")


def validate_username(username):
    if USERNAME_REGEX.match(username) is not None:
        return "valid"
    return "Username should be at least 3 characters long and\
 may only contain letters, numbers, '-', '.' and '_'"


def validate_password(password):
    if PASSWORD_REGEX.match(password) is not None:
        return "valid"
    return "Password should be at least 6 characters long and\
 must contain at least 1 uppercase letter, 1 lowercase letter and 1 number"


def validate_user_email(email):
    try:
        validate_email(email)
    except Exception as e:
        return str(e)
    return "valid"
