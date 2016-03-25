from hashlib import md5


def hass_password(password):
    return md5(password).hexdigest()


def mail_row_to_dict(mail_item):
    return {'id': mail_item.id,
            'sender_id': mail_item.sender_id,
            'recipient': mail_item.recipient,
            'subject': mail_item.subject,
            'text': mail_item.text,
            'timestamp': mail_item.timestamp,
            'status': mail_item.status,
            'is_viewed': mail_item.is_viewed}