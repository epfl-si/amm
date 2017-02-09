#!/bin/bash

flake8 --exclude=migrations,.idea/ --max-line-length=120 ./src

