import os

basedir = os.path.abspath(os.path.dirname(__file__))

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URI', 'Database URI')
}

AppConfig = {
    'MAIL_DOMAIN': 'csit.edu',
    'SECRET_KEY': os.urandom(32),
    'DEBUG_MODE': True,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000))
}

MailConfig = {
    'SENDGRID_API_KEY': os.getenv('SENDGRID_API_KEY', 'Sendgrid API key')
}
