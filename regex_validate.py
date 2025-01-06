import re

# Validate strong password
password_pattern = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
username_pattern= re.compile(r"^[a-zA-Z0-9]{10,}$")


def is_validate_password(password):
    return bool(password_pattern.match(password))

def is_validate_username(username):
    return bool(username_pattern.match(username))


# def is_validate_password(password):
#     if len(password) >=20:
#         return True
#     return False

# def is_validate_username(username):
#     if len(username) >= 10:
#         return True
#     return False
