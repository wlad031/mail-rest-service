from hashlib import md5


def hass_password(password):
    return md5(password).hexdigest()
