import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db, cfg
from helper import hass_password


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    pass_hash = db.Column(db.String(32))
    is_authenticated = True
    is_active = True

    def __init__(self, username, password):
        self.username = username
        self.pass_hash = hass_password(password)

    def verify_password(self, password):
        return hass_password(password) == self.pass_hash

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self, expiration=86400):
        s = Serializer(cfg.AppConfig['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(cfg.AppConfig['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.query.get(data['id'])
        return user


class MailStatus(db.Enum):
    draft = 'draft'
    sent = 'sent'

    @staticmethod
    def get_statuses():
        return [MailStatus.sent, MailStatus.draft]


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(128))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    status = db.Column(MailStatus, default=MailStatus.sent)
    is_viewed = db.Column(db.Boolean, default=False)

    sender = db.relationship(User, foreign_keys='Mail.sender_id')
    recipient = db.relationship(User, foreign_keys='Mail.recipient_id')

    def __init__(self, sender_id, recipient_id, subject, text, status):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.subject = subject
        self.text = text
        self.status = status

    def __repr__(self):
        return '<Mail %r>' % self.text


class MailOwner(db.Model):
    __tablename__ = 'mail_owner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, mail_id, user_id):
        self.mail_id = mail_id
        self.user_id = user_id
