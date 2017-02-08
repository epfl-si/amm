#!/bin/bash

rm -rf ../docker/django/requirements
cp -r ../requirements ../docker/django
cd ..
docker-compose build