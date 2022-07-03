How to use this project

Create a new directory for your project and do a git checkout

    mkdir -p /path/to/project && cd /path/to/project
    git clone git@github.com:hartleybrody/flask-boilerplate.git

Then you can move the files out of the `flask-boilerplate` directory and into `/path/to/project` using

    cp -r flask-boilerplate/. .

Finally, delete the `flask-boilerplate` directory and start it as a new git repo

    rm -rf flask-boilerplate
    rm -rf .git && git init
    git add .
    git commit -m "initial import from flask boilerplate"

To make this template fit your app, replace the following

 * {{APP_NAME}} -> App Name
 * {{APP_SLUG}} -> app-name
 * {{APP_BLURB}} -> Here is a quick blurb about the app

=====================

# {{APP_NAME}}
{{APP_BLURB}}

### Local configuration
This project uses [python-dotenv](https://github.com/theskumar/python-dotenv) to read configuration from a `.env` file.

Note that while `.env` is initially provided for you, any configuration information you put in there should NOT be committed. Let's remove it from git tracking.

    git rm -r --cached .env

### Install python dependencies
Install the essential libraries for this project.

    poetry install

This will install all of the dependencies that are defined in `pyproject.toml` -- as [also specified in the `poetry.lock` file](https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control).

### Setup local postgres and redis
This project uses the pattern of having `docker-compose.yml` specify the backing services (postgres and redis databases) while letting the application run directly on the host so it's easier to interact with.

Create a postgres and redis database with

    docker-compose up

Note that if you make any changes to the Dockerfile or `docker-compose.yml`, you may need to "rebuild" by adding the `--build` flag. You don't need to use this every time you bring the containers up though, since you can usually reuse the previously built images, which is much faster.

     docker-compose up --build

DANGER: If you really, really need to burn your environment and start from scratch (say, to reinitialize the `pgdata` docker volume for the database for some reason), you can run `docker system prune` and then `docker volume rm` the pgdata volume.


### Initial database setup
Once you've created a brand new database, apply the existing migrations to get your database tables setup properly

    poetry run flask db upgrade

Note that the current schema is defined in `models.py` and the migrations live in `migrations/versions` (see below)

You'll also need to do an initial "seed" command to add some placeholder rows to the database

    poetry run flask seed

### Run your local server
Run the local flask development server (automatically reloads changes) with

    flask run

or alternatively, use the production server gunicorn

    gunicorn app:app --reload --bind 127.0.0.1:5000

Either way, your local development server should be viewable in a browser

    http://localhost:5000

### Running your local server over SSL (optional)
Running your local development server over SSL is optional but highly recommended since it makes your local env closer to prod, and allows you to catch potential content issues sooner. I recommend [mkcert](https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/) for creating browser-trusted, self-signed certificates.

First, install mkcert

    brew install mkcert
    brew install nss

Then, allow it to install a locally-trusted CA

    mkcert -install

Finally, generate a certificate for the local domain you'll be using:

    mkcert {{APP_SLUG}}.local

This will generate a certificate and key in the current directory. You can move them wherever you like, just make sure to update the env variables to point to their file system location, and then uncomment out the line at the very bottom of `app.py` that tells your local server to use them.

    app.run(debug=True, ssl_context=(os.environ["LOCAL_SSL_CERT_PATH"], os.environ["LOCAL_SSL_KEY_PATH"]))

Alternatively, you can run your local flask development server with

    flask run --cert=$LOCAL_SSL_CERT_PATH --key=$LOCAL_SSL_KEY_PATH

In order to access the local development server with the correct SSL certificates, you'll need to create an entry in your HOSTS file that points `local.{{APP_SLUG}}.com` at the regular loopback interface (127.0.0.1)

On macOS, you can add an entry to your HOSTS file with:

    sudo vim /etc/hosts

and then append a line to the end of the file that looks like

     127.0.0.1 {{APP_SLUG}}.local

Then exit vim with the famous `esc` + `:wq` and you should be able to visit the site over SSL in your browser at

    https://{{APP_SLUG}}.local:5000


### Run database migrations
Detect changes to `models.py` and generate a timestamped migration file

    flask db migrate

Once you've looked over the generated migrations file, apply the migration to your local database

    flask db upgrade

To roll back the most recent migration that has been applied to the database (maybe due to errors or changes)

    flask db downgrade

### Testing
You'll need to set up a separate postgres database for testing

    psql -h localhost -d postgres

    psql (13.1)
    Type "help" for help.

    postgres=# CREATE DATABASE {{APP_SLUG}}_test;
    CREATE DATABASE

To run the tests

    python test.py


### Deploying
To push code changes to heroku

    git push heroku master

To run database migrations on heroku

    heroku run flask db upgrade

Make sure you run this immediately after deploying any code that includes database migrations.