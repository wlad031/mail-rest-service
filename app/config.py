import os

basedir = os.path.abspath(os.path.dirname(__file__))

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': (
        os.getenv('DATABASE_URI',
                  'postgres://orveamykispgam:zVvcgvwlPO0OKR3rXyeB7LwsyT@ec2-107-22-246-250.compute-1.amazonaws.com:5432/deeg08griam59u')
    ),
}

AppConfig = {
    'SECRET_KEY': os.urandom(32),
    'DEBUG_MODE': False,
    'HOST': os.getenv('HOST', '0.0.0.0'),
    'PORT': int(os.getenv('PORT', 5000))
}
