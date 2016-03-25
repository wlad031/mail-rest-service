import os

basedir = os.path.abspath(os.path.dirname(__file__))

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': (
        os.getenv('DATABASE_URI', 'mysql://root:password@localhost:3306/mail')
    ),
}

AppConfig = {
    'MAIL_DOMAIN': 'csit.edu',
    'SECRET_KEY': os.urandom(32),
    'DEBUG_MODE': True,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000))
}

MailConfig = {
    'MAIL_SERVER': 'smtp.gmail.com:587',
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD')
}
