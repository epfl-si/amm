#!/bin/bash

docker build --no-cache --build-arg REQUIREMENTS_FILE='requirements/local.txt' --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 . -t epflidevelop/amm-dev

docker build --no-cache --build-arg REQUIREMENTS_FILE='requirements/prod.txt' --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 . -t epflidevelop/amm
