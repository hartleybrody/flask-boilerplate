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

### Install python dependencies
This project assumes you already have [direnv](https://github.com/direnv/direnv) installed globally on your system.

    brew install direnv

The first time you `cd` into the project directory, direnv will take a minute to set things up, including automatically creating a new virtual environment. It will use python3 since this is specified in the `.envrc` file.

Once it's done, install the essential libraries for this project.

    pip install -r requirements.txt

Optional: Once installed, you can snapshot the version of each library and override the contents of that file by pinning their version numbers. This is good practice to ensure you start your project with the latest version of each dependency, but then don't have to worry about new versions causing breaking changes down the line.

    pip freeze > requirements.txt

### Setup local postgres database
Create the database locally

    psql -h localhost -d postgres

    psql (13.1)
    Type "help" for help.

    postgres=# CREATE DATABASE {{APP_SLUG}};
    CREATE DATABASE

### Initial database setup
Once you've created a brand new database, apply the existing migrations to get your database tables setup properly

    flask db upgrade

Note that the current schema is defined in `models.py` and the migrations live in `migrations/versions` (see below)

You'll also need to do an initial "seed" command to add some placeholder rows to the database

    flask seed


### Setup local redis server
Most web applications can benefit from an in-memory cache. They're great for server-side sessions and also for taking load off the database.

You can install redis using [the project's Quickstart instructions](https://redis.io/topics/quickstart).

Or, if you're on macOS with homebrew, you can simply run

    brew install redis

Once you've got redis installed on your system, start the local server in the background with

    redis-server  --daemonize yes

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

    mkcert local.{{APP_SLUG}}.com

This will generate a certificate and key in the current directory. You can move them wherever you like, just make sure to update the env variables to point to their file system location, and then uncomment out the line at the very bottom of `app.py` that tells your local server to use them.

    app.run(debug=True, ssl_context=(os.environ["LOCAL_SSL_CERT_PATH"], os.environ["LOCAL_SSL_KEY_PATH"]))

In order to access the local development server with the correct SSL certificates, you'll need to create an entry in your HOSTS file that points `local.{{APP_SLUG}}.com` at the regular loopback interface (127.0.0.1)

On macOS, you can add an entry to your HOSTS file with:

    sudo vim /etc/hosts

and then append a line to the end of the file that looks like

     127.0.0.1 local.{{APP_SLUG}}.com

Then exit vim with the famous `esc` + `:wq` and you should be able to visit the site over SSL in your browser at

    https://local.{{APP_SLUG}}.com:5000

Once you've gotten SSL setup and running locally, you can add a "Hyper-Strict Transport Security" (HSTS) header to force the browser to always request the site over SSL. Simply uncommenting out the line in app.py that looks like

    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains

**WARNING**: Once you uncomment this header and visit the site, your browser will *always* request the site over SSL for one year and there is *no way to force your browser to request the site over plain ol' HTTP*. This is a good security best practice, but can present a mucky situation if you haven't gotten the SSL setup stuff figured out.


### Run database migrations
Detect changes to `models.py` and generate a timestamped migration file

    flask db migrate -m "migration summary"

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

============================================================

## Alternatively, use Docker


### Setup local environment with docker compose

## build the frontend
Create the frontend

    docker-compose up

Note that if you make any changes to the Dockerfile or change the requirements.txt file, you'll need to "rebuild" by adding the `--build` flag. You don't need to use this every time you bring the containers up though, since you can usually reuse the previously built images, which is much faster.

     docker-compose up --build

DANGER: If you really, really need to burn your environment and start from scratch (say, to reinitialize the `pgdata`docker volume for the database for some reason), you can run `docker system prune` and then `docker volume rm` the pgdata volume.

## run commands inside docker container
Since docker-compose specifies that the default entrypoint always starts with `flask` you can run any arbitrary flask CLI command inside the docker container by passing that command to the `docker-compose run web` prefix. For example:

create a migration using the docker container

    docker-compose run web db migrate -m "migration summary"

run database migrations using docker

    docker-compose run web db upgrade

downgrade the database using docker

    docker-compose run web db downgrade

seed the database using... you get it.

    docker-compose run web seed

## other helpful docker tips & tricks

You can follow the logs for the container with

    docker logs -f web

You can "ssh into" a running container with

    docker exec -it web /bin/bash

You can inspect the database inside the container with

    docker exec -it db psql $DATABASE_URL

You can inspect the cache inside the container with

    docker exec -it cache redis-cli

    127.0.0.1:6379> KEYS *