import os

basedir = os.path.abspath(os.path.dirname(__file__))

MySQLConfig = {
    'USER': 'root',
    'PASSWORD': 'password',
    'DB': 'mail',
    'HOST': '127.0.0.1',
    'PORT': '3306'
}

DatabaseConfig = {
    'SQLALCHEMY_DATABASE_URI': (
        'mysql://' + MySQLConfig['USER'] +
        ':' + MySQLConfig['PASSWORD'] +
        '@' + MySQLConfig['HOST'] +
        ':' + MySQLConfig['PORT'] +
        '/' + MySQLConfig['DB']
    ),

    'SQLALCHEMY_MIGRATE_REPO': os.path.join(basedir, 'db_repository')
}


AppConfig = {
    'SECRET_KEY': '8efbdcc5351b3417502c8d562a144fc1',
    'DEBUG_MODE': True,
    'HOST': '0.0.0.0',
    'PORT': int(os.environ.get("PORT", 5000))
}
