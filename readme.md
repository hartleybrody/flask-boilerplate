Actual readme for this project:

To make this template fit your app, replace the following

 * {{APP_NAME}} -> App Name
 * {{APP_SLUG}} -> app-name
 * {{APP_BLURB}} -> Here is a quick blurb about the app

=====================

# {{APP_NAME}}
{{APP_BLURB}}

### Install python dependencies
This project assumes you already have [virtualenv, virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and [autoenv](https://github.com/kennethreitz/autoenv) installed globally on your system.

First, create a new virtual environment:

    mkvirtualenv {{APP_SLUG}}

Then, install the required python dependencies

    pip install -r requirements.txt

### Setup local postgres database
Create the database locally

    psql -h localhost -d postgres

    psql (10.1)
    Type "help" for help.

    postgres=# CREATE DATABASE {{APP_SLUG}};
    CREATE DATABASE


### Setup local redis server
Most web applications can benefit from an in-memory cache. They're great for server-side sessions and also for taking load off the database.

You can install redis using [the project's Quickstart instructions](https://redis.io/topics/quickstart).

Or, if you're on macOs with homebrew, you can simply run

    brew install redis

Once you've got redis installed on your system, start the local server in the background with

    redis-server  --daemonize yes

### Run your local server
Ensure that the local `.env` file has been applied, then run

    python app.py

or alternatively, use gunicorn

    gunicorn app:app --reload --bind 127.0.0.1:5000

### Running your local server over SSL (optional)
Running your local development server over SSL is optional but highly recommended since it makes your local env closer to prod, and allows you to catch potential content issues sooner. I recommend [mkcert](https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/) for creating browser-trusted, self-signed certificates.

First, install mkcert

    brew install mkcert
    brew install nss

Then, allow it to install a locally-trusted CA

    mkcert -install

Finally, generate a certificate for the local domain you'll be using:

    mkcert local.{{APP_SLUG}}.com

This will generate a certificate and key in the current directory. You can move them wherever you like, just make sure to update the env variables to point to their file system location, and then uncomment out the line at the very bottom of `app.py` that tells your local server to use them.

    app.run(debug=True, ssl_context=(os.environ["LOCAL_SSL_CERT_PATH"], os.environ["LOCAL_SSL_KEY_PATH"]))


### Run database migrations
Detect changes to `models.py` and generate a timestamped migration file

    python manage.py db migrate

Once you've looked over the generated migrations file, apply the migration to your local database

    python manage.py db upgrade

To roll back the most recent migration that has been applied to the database (maybe due to errors or changes)

    python manage.py db downgrade -1

### Testing
You'll need to set up a separate postgres database for testing

    psql -h localhost -d postgres

    psql (9.4.4)
    Type "help" for help.

    postgres=# CREATE DATABASE {{APP_SLUG}}_test;
    CREATE DATABASE

To run the tests

    python test.py


### Deploying
To push code changes to heroku

    git push heroku master

To run database migrations on heroku

    heroku run python manage.py db upgrade

Make sure you run this immediately after deploying any code that includes database migrations.

