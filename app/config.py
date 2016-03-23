import os

basedir = os.path.abspath(os.path.dirname(__file__))

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': (
        os.getenv('DATABASE_URI', 'mysql://sql7111851:ljXnHgXURP@sql7.freemysqlhosting.net:3306/sql7111851')
    ),
}

AppConfig = {
    'SECRET_KEY': os.urandom(32),
    'DEBUG_MODE': False,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000))
}
