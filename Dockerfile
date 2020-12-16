FROM python:3.8

WORKDIR /app

ADD . /app

RUN pip install -U flask

WORKDIR /app/app

CMD [ "python", "app.py" ]

