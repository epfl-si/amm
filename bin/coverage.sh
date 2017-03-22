#!/bin/bash -e

coverage run --source='.' src/manage.py test --settings=config.settings.local --exclude-tag=rancher
coverage html
