import re

# Validate strong password
password_pattern = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
username_pattern= re.compile(r"^[a-zA-Z0-9]{10,}$")


ipv4_regex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

ipv6_regex = re.compile(r'^(([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)|(([0-9a-fA-F]{1,4}:){1,6}|:):([0-9a-fA-F]{1,4}|:){1,6}|::([0-9a-fA-F]{1,4}:){0,5}([0-9a-fA-F]{1,4}|:)|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$')

def is_validate_password(password):
    return bool(password_pattern.match(password))

def is_validate_username(username):
    return bool(username_pattern.match(username))


def is_valid_ipv4(ip):
    return bool(ipv4_regex.match(ip))

def is_valid_ipv6(ip):
    return bool(ipv6_regex.match(ip))
