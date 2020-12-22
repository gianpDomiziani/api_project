FROM python:3.8-alpine



RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq
RUN apk del --no-cache .build-deps

RUN python3 -m pip3 install pip3 --upgrade pip

WORKDIR /home

ADD . /home

RUN pip3 install -r requirements.txt

WORKDIR /home/app

ENV FLASK_APP=app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1

CMD flask run --host=0.0.0.0 --port=80