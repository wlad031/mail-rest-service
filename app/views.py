import datetime
import smtplib

from flask import jsonify, request, g
from flask.ext.httpauth import HTTPBasicAuth
from email import message

from app import app, db, cfg
from app.models import User, Mail, MailOwner, MailStatus
from helper import mail_row_to_dict

# Authentication

auth = HTTPBasicAuth()


@app.route('/api/user', methods=['PUT'])
def new_user():
    username = request.json.get('username') + '@' + cfg.AppConfig['MAIL_DOMAIN']
    password = request.json.get('password')

    c = check_user_fields(username, password)
    if c is not None:
        return c

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'username': user.username}), 201


@app.route('/api/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify({'id': user.id, 'username': user.username}), 200


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'id': g.user.id,
                    'username': g.user.username,
                    'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)

    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


# Mails

@app.route('/api/mail/available_statuses')
def available_statuses():
    return jsonify({'statuses': MailStatus.get_statuses()})


@app.route('/api/mail/<int:mail_id>', methods=['GET'])
@auth.login_required
def get_mail(mail_id):
    mail = get_my_mail_by_id(mail_id)

    if mail is None:
        return jsonify({'error': 'Mail not found'}), 404

    return jsonify({'mail': mail_row_to_dict(mail)})


@app.route('/api/mail', methods=['GET'])
@auth.login_required
def get_all_mails():
    mails = list([mail_row_to_dict(m) for m in Mail.query.filter(Mail.id.in_(get_my_mail_ids())).all()])
    return jsonify({'mails': mails})


@app.route('/api/mail', methods=['PUT'])
@auth.login_required
def create_mail():
    recipient_name = request.json.get('recipient')
    subject = request.json.get('subject')
    text = request.json.get('text')
    status = request.json.get('status')

    rec = recipient_name.split('@', 1)

    c = check_mail_status(status)
    if c is not None:
        return c

    mail = Mail(sender_id=g.user.id,
                recipient=recipient_name,
                subject=subject,
                text=text,
                status=status)

    db.session.add(mail)
    db.session.commit()

    db.session.add(MailOwner(user_id=g.user.id, mail_id=mail.id))
    db.session.commit()

    if rec[1] == cfg.AppConfig['MAIL_DOMAIN']:
        if status == MailStatus.sent:
            recipient = User.query.filter_by(username=recipient_name).first()
            if recipient is not None:
                db.session.add(MailOwner(user_id=recipient.id, mail_id=mail.id))
                db.session.commit()

    else:
        msg = message.Message()
        msg.add_header('from', g.user.username)
        msg.add_header('to', recipient_name)
        msg.add_header('subject', subject)
        msg.set_payload(text)

        server = smtplib.SMTP(cfg.MailConfig['MAIL_SERVER'])
        server.starttls()
        server.login(cfg.MailConfig['MAIL_USERNAME'], cfg.MailConfig['MAIL_PASSWORD'])

        server.sendmail(g.user.username, recipient_name, msg.as_string())
        server.close()

    return jsonify({'process': 'create', 'result': True, 'mail': mail_row_to_dict(mail)}), 201


@app.route('/api/mail/<int:mail_id>', methods=['PUT'])
@auth.login_required
def update_mail(mail_id):
    recipient_name = request.json.get('recipient')
    subject = request.json.get('subject')
    text = request.json.get('text')
    status = request.json.get('status')
    is_viewed = request.json.get('is_viewed')

    mail = get_my_mail_by_id(mail_id)

    if mail is None:
        return send_error('Mail not found', 404)

    updating_data = {'timestamp': datetime.datetime.now().isoformat()}

    if subject is not None:
        updating_data['subject'] = subject
    if text is not None:
        updating_data['text'] = text
    if status is not None:
        if not check_mail_status(status):
            return send_error('invalid status', 400)
        updating_data['status'] = status
    if is_viewed is not None:
        updating_data['is_viewed'] = is_viewed

    Mail.query.filter_by(id=mail_id).update(updating_data)

    if status == 'send':
        recipient = User.query.filter_by(username=recipient_name).first()
        if recipient is not None:
            db.session.add(MailOwner(user_id=recipient.id, mail_id=mail.id))

    db.session.commit()

    return jsonify({'process': 'update', 'result': True, 'mail': mail_row_to_dict(mail)}), 200


@app.route('/api/mail/<int:mail_id>', methods=['DELETE'])
@auth.login_required
def delete_mail(mail_id):
    mail = get_my_mail_by_id(mail_id)

    if mail is None:
        return send_error('Mail not found', 404)

    MailOwner.query.filter_by(user_id=g.user.id, mail_id=mail_id).delete()
    db.session.commit()

    return jsonify({'process': 'delete', 'result': True, 'mail_id': mail_id}), 200


def get_my_mail_by_id(mail_id):
    return Mail.query.filter(Mail.id.in_(get_my_mail_ids())).filter_by(id=mail_id).first()


def get_my_mail_ids():
    return [mtu.mail_id for mtu in MailOwner.query.filter_by(user_id=g.user.id).all()]


def check_mail_status(status):
    if status not in MailStatus.get_statuses():
        return send_error('Wrong mail status', 400)


def check_user_fields(username, password):
    missing = []
    if username is None:
        missing.append('username')
    if password is None:
        missing.append('password')

    if len(missing) > 0:
        return send_error('Missing arguments', 400, args=missing)

    if User.query.filter_by(username=username).first() is not None:
        return send_error('User with the same name is already exists', 400)

    return None


def send_error(message, status_code, args=None, description=None):
    return jsonify({'error': message, 'args': args, 'description': description}), status_code
