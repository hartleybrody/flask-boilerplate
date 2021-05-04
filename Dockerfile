FROM python:3.8.9

#FROM python:alpine3.7
#RUN apk update
#RUN apk add postgresql-dev gcc python3-dev musl-dev
#RUN \
# apk add --no-cache postgresql-libs && \
# apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# EXPOSE 80
EXPOSE 8080

WORKDIR /flask-app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "--log-file=-", "-b 0.0.0.0:80"]

#ENTRYPOINT [ "python" ]
#CMD [ "app.py" ]