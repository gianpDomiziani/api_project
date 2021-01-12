#!/bin/bash
appname="api_project"
docker stop $appname
docker rm --force $appname
echo "COMMAND> docker build . -t $appname"
docker build . -t $appname
echo "COMMAND> docker container run -p 5000:8080 --name $appname $appname"
docker container run -p 5000:8080 --name $appname $appname