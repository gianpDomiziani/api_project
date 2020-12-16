FROM python:3.8

WORKDIR /home

ADD . /home

RUN pip install -U flask

WORKDIR /home/app

CMD [ "python", "app.py" ]

