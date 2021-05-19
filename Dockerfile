# syntax=docker/dockerfile:1
FROM python:3.9.5

WORKDIR /flask-app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# used by gunicorn https://docs.gunicorn.org/en/stable/settings.html#bind
# ENV PORT 80

# allows for passing extra flags to gunicorn at container runtime
# https://phoenixnap.com/kb/docker-cmd-vs-entrypoint
# ENTRYPOINT [ "gunicorn", "app:app" ]

ENV FLASK_ENV "development"
ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0", "--port=80", "--reload"]