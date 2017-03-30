import requests

from config.settings import base

ACCRED_URL = "https://test-websrv.epfl.ch/rwsaccred/getRights"
DB_ADMIN_RIGHT_ID = 100


def is_db_admin(user_id, unit_id):
    """
    Returns true if the given user has the db admin role in the given unit.
    """

    # url params
    params = {
        "app": "AMM",
        "caller": "000000",
        "password": base.get_config('ACCRED_PASSWORD'),
        "rightid": DB_ADMIN_RIGHT_ID,
        "unitid": unit_id
    }

    response = requests.get(ACCRED_URL, params)

    result = response.json()["result"]

    for result_id in result:
        if user_id == str(result_id):
            return True

    return False
