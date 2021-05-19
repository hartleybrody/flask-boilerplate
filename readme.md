Actual readme for this project:

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

The first time you `cd` into the project directory, direnv will take a minute to set things up, including automatically creating a new virtual environment.

Once it's done, install the essential libraries for this project.

    pip install -r requirements.txt

Optional: Once installed, you can snapshot the version of each library and override the contents of that file by pinning their version numbers

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

### Setup local environment with docker
Run `docker build` to build an image from the `Dockerfile`

    docker build --tag {{APP_SLUG}} .

Verify the image was created by running `docker images`

Then you can actually run your image as a container with

    docker run -p 8000:80 --env-file .env --name web {{APP_SLUG}}    # todo, use docker compose instead of --env-file

Add the `-d` flag just  before `{{APP_SLUG}}` to detach and run the container in the background

Note that the `docker run` command is equivalent to running `docker create` + `docker start` + `docker attach`

Verify the container is working by running `docker ps` in a different terminal tab

Verify that the app loads with

    curl localhost:8000

You can follow the logs for the container with

    docker logs -f web

You can "ssh into" a running container with

    docker exec -it web /bin/bash

