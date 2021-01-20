#  #!/usr/bin python

#  Copyright (c) 2020.  Dave Davis
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Init settings
import sys

import requests
import pprint
from dg_adobe.adobe_authenticate import adobe_analytics_auth
from dg_adobe.report_types import get_report_type
from dg_config import settingsfile

from dg_db.db_write import write_adobe_report_to_db

settings = settingsfile.get_settings()


def get_report(date_range, report_type):
    # Authenticate
    access_token, global_company_id = adobe_analytics_auth()

    # Get the report type back as a a query string so we can edit the date ranges and metrics.
    query = get_report_type(report_type, date_range)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(query)

    # Add reports to a list
    records_to_insert = []

    # Get the report data
    # ToDo: Reformat using fstrings
    adobe_report_response = requests.post(
        "{}/{}/reports".format(settings["analytics_api_url"], global_company_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
            'x-api-key': settings["api_key"],
            'x-proxy-global-company-id': global_company_id,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=query
    )
    # ToDo: Add more error checking here, particularly around error codes (403)

    #################################################################################################
    #################################################################################################
    # This is where I left off. Response is being returned, now just need to parse and write to DB  #
    #################################################################################################
    #################################################################################################


    if adobe_report_response.json() is not None:
        # return adobe_report_response.json()
        print(adobe_report_response.json())
        # Send the list off to be written.
        write_adobe_report_to_db(records_to_insert, report_type)


