import configparser
import csv
import datetime
import json
import logging
import os
from time import sleep
import jwt
import requests

# Set up logging.
# ToDo: Replace with Rich and prettyerrors
from dg_config import settingsfile

logging.basicConfig(level="INFO")
logger = logging.getLogger()

# Set up settings
settings = settingsfile.get_settings()

def adobe_analytics_auth():
    # Get JWT token and store access token for reporting API requests.
    jwt_token = get_jwt_token()
    logger.info("JWT Token: {}".format(jwt_token))

    access_token = get_access_token(jwt_token)
    logger.info("Access Token: {}".format(access_token))

    global_company_id = get_first_global_company_id(access_token)
    logger.info("global company is: {}".format(global_company_id))

    return access_token, global_company_id



def get_jwt_token():
    with open(os.path.join(os.getcwd(), settings['key_file']), 'rb') as f:
        private_key = f.read()

    return jwt.encode({
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        "iss": settings["org_id"],
        "sub": settings["technical_account_id"],
        "https://{}/s/{}".format(settings["ims_host"], settings["metascopes"]): True,
        "aud": "https://{}/c/{}".format(settings["ims_host"], settings["api_key"])
    }, private_key, algorithm='RS256')


def get_access_token(jwt_token):
    post_body = {
        "client_id": settings["api_key"],
        "client_secret": settings["secret"],
        "jwt_token": jwt_token
    }
    logger.info("Sending 'POST' request to {}".format(settings["ims_exchange"]))
    # logger.info("Post body: {}".format(post_body))

    response = requests.post(settings["ims_exchange"], data=post_body)
    return response.json()["access_token"]


def get_first_global_company_id(access_token):
    response = requests.get(
        settings["discovery_url"],
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "x-api-key": settings["api_key"]
        }
    )

    # Return the first global company id
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.", response.json().get("imsOrgs")[0].get("companies")[0].get("globalCompanyId"))
    return response.json().get("imsOrgs")[0].get("companies")[0].get("globalCompanyId")



def get_users_me(global_company_id, access_token):
    response = requests.get(
        "{}/{}/users/me".format(settings["analytics_api_url"], global_company_id),
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "x-api-key": settings["apikey"],
            "x-proxy-global-company-id": global_company_id
        }
    )
    return response.json()