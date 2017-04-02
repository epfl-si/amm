"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import requests

from config.settings import base


def is_db_admin(user_id, unit_id):
    """
    Returns true if the given user has the db admin role in the given unit.
    """

    ACCRED_URL = "https://test-websrv.epfl.ch/rwsaccred/getRights"
    DB_ADMIN_RIGHT_ID = 100

    # url params
    params = {
        "app": "AMM",
        "caller": "000000",
        "password": base.get_config('ACCRED_PASSWORD'),
        "rightid": DB_ADMIN_RIGHT_ID,
        "unitid": unit_id
    }
    result = requests.get(ACCRED_URL, params).json()["result"]
    return user_id in [str(result_id) for result_id in result]


def get_accreditations_units(user_id):
    """"
    Return all accreditations units of user 'user_id'
    """

    ACCRED_URL = "https://test-websrv.epfl.ch/rwspersons/getPerson"

    # url params
    params = {
        "app": "AMM",
        "caller": "000000",
        "password": base.get_config('ACCRED_PASSWORD'),
        "id": user_id
    }
    accreditations = requests.get(ACCRED_URL, params).json()["result"]["accreds"]
    return [accred["accred"]["id"].split(":")[0] for accred in accreditations]
