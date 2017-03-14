#!/bin/bash -e

coverage run --source='.' src/manage.py test --settings=config.settings.local
#api.tests.test_views.ViewsTestCase.test_get_apikeys
coverage html
