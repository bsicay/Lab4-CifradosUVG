REGISTER_SCHEMA = {
    'email': {'required': True, 'type': str},
    'password': {'required': True, 'type': str}
}

LOGIN_SCHEMA = {
    'email': {'required': True, 'type': str},
    'password': {'required': True, 'type': str}
}

REFRESH_SCHEMA = {
    'refresh_token': {'required': True, 'type': str}
}