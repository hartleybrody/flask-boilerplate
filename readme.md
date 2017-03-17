# {{APP_NAME}}
{{APP_BLURB}}

### install python dependencies

    pip install -r requirements.txt

### setup local database
create the database locally

    psql -h localhost -d postgres

    psql (9.4.4)
    Type "help" for help.

    postgres=# CREATE DATABASE {{APP_SLUG}};
    CREATE DATABASE

if this is a brand new app, run the initial alembic setup

    python manage.py db init

### run the local server
ensure that the local `.env` file has been applied, then run

    python app.py

or alternatively, use gunicorn

    gunicorn app:app --reload

### run database migrations
detect changes to `models.py` and generate a migration file

    python manage.py db migrate

once you've looked over the generated migrations file, run the migration

    python manage.py db upgrade

### deploying
to push code changes to heroku

    git push heroku master

to run database migrations on heroku

    heroku run python manage.py db upgrade

