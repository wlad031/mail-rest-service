# Mail-Server
Study project of the subject "Software testing"

#### Usage
Install dependencies:

    pip install -r requirements.txt


Set environment variables:

    export HOST="<Host address>" # otherwise it will use localhost
    export PORT="<Port on which app will be deployed>" # otherwise it will use 5000
    export SENDGRID_API_KEY="<Your Sendgrid API key>" # required
    export DATABASE_URI="<sql>://<username>:<password>@<host>:<port>/<database>" # required
    

Migrate database schema:

    python migrate.py db init
    python migrate.py db migrate
    python migrate.py db upgrade

Run:

    python run.py
