from flask import jsonify, request, abort, g
from flask.ext.httpauth import HTTPBasicAuth

from app import app, db
from app.models import User

auth = HTTPBasicAuth()


@app.errorhandler(401)
def error_401(error):
    return jsonify({'error': 'Unauthorized access'}), 401


@app.route('/api/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return jsonify({'error': 'Missing arguments'}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'User with the same name is already exists'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'username': user.username}), 201


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


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
