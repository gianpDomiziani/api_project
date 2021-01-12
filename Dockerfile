FROM python:3.7-slim-buster

WORKDIR /home
COPY . /home
RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "server.py" ]