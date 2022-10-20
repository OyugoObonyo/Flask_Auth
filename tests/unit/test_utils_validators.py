import pytest
from utils.validators import (validate_user_email,
                              validate_password, validate_username)


@pytest.mark.parametrize(
    "email, output",
    [
        ("user@email.com", "valid"),
        ("user.com", "The email address is not valid. It must have exactly one @-sign."),
        ("user@testuser.com", "The domain name testuser.com does not send email.")
    ]
)
def test_validate_user_email(email, output):
    assert validate_user_email(email) == output


@pytest.mark.parametrize(
    "password, output",
    [
        ("notavalidpassword", "Password should be at least 6 characters long\
 and must contain at least 1 uppercase letter, 1 lowercase letter and 1 number"),
        ("Astrong!Password001", "valid"),
        ("S8ort", "Password should be at least 6 characters long\
 and must contain at least 1 uppercase letter, 1 lowercase letter and 1 number"),
        ("NosPecialCharact8", "valid")
    ]
)
def test_password_validity(password, output):
    assert validate_password(password) == output


@pytest.mark.parametrize(
    "username, output",
    [
        ("me", "Username should be at least 3 characters long and\
 may only contain letters, numbers, '-', '.' and '_'"),
        ("User_99", "valid"),
        ("peter-98.py", "valid"),
        ("Notauser!", "Username should be at least 3 characters long and\
 may only contain letters, numbers, '-', '.' and '_'")
    ]
)
def test_username_validity(username, output):
    assert validate_username(username) == output
