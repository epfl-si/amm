#!/bin/bash -e

coverage run --source='.' src/manage.py test --settings=config.settings.local api.tests.test_rancher.RancherTest.test_create_mysql_stack
coverage html
