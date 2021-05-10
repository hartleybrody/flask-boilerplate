FROM python:3.9.5

WORKDIR /flask-app

COPY . .

RUN pip install -r requirements.txt

# used by gunicorn https://docs.gunicorn.org/en/stable/settings.html#bind
ENV PORT 80

# allows for passing extra flags to gunicorn at container runtime
# https://phoenixnap.com/kb/docker-cmd-vs-entrypoint
ENTRYPOINT [ "gunicorn", "app:app" ]