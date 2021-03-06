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
import datetime
import json
import math
import sys
from time import strftime, sleep

import requests
import pprint
from dg_adobe.adobe_authenticate import adobe_analytics_auth
from dg_adobe.report_types import get_report_type
from dg_config import settingsfile
from dg_db.db_write import write_adobe_report_to_db
from rich.console import Console
import pandas as pd

console = Console()
settings = settingsfile.get_settings()


def get_report(adobe_full_date_range, report_type):
    # Authenticate
    access_token, global_company_id = adobe_analytics_auth()

    # List of RSIDs to loop through.
    rsids = settings["rsids"]

    # Container for returned records.
    records_to_insert = []

    for rsid in rsids:
        # Get the report type and query string.
        query = get_report_type(report_type, adobe_full_date_range, rsid)

        # Get the report data
        adobe_report_response = requests.post("{}/{}/reports".format(settings["analytics_api_url"], global_company_id),
                                              headers={'Authorization': 'Bearer {}'.format(access_token),
                                                       'x-api-key': settings["api_key"],
                                                       'x-proxy-global-company-id': global_company_id,
                                                       'Accept': 'application/json',
                                                       'Content-Type': 'application/json'},
                                              data=query)

        # ToDo: Add more error checking here, particularly around error codes (403)

        # Take the response and convert it into a list with only the data that we want.
        if adobe_report_response.json() is not None:
            response_dict = adobe_report_response.json()
            # Check for existence of rows
            if response_dict["rows"]:
                # Loop through the Adobe record and pluck out what we need into a cleaned record list.
                for record in response_dict["rows"]:
                    cleaned_record = [rsid, record["value"],
                                      record["data"][0], record["data"][1],
                                      record["data"][2], record["data"][3],
                                      record["data"][4], record["data"][5],
                                      record["data"][6]]

                    if cleaned_record[3] == "NaN":
                        cleaned_record[3] = 0
                    if cleaned_record[6] == "NaN":
                        cleaned_record[6] = 0
                    if cleaned_record[8] == "NaN":
                        cleaned_record[8] = 0

                    # Finally, add the cleaned record list to the list we want to pass to the DB write module.
                    records_to_insert.append(cleaned_record)
            else:
                console.print("A response was received from the Adobe API but it contained no data", style="bold red")

        # As we're calling many daily reports, we'll be rate limited. So adding in a delay here.
        sleep(settings["adobe_api_delay"])
        console.print(records_to_insert)

    # Send the list off to be written.
    # ToDo: Reset this
    write_adobe_report_to_db(records_to_insert, report_type)
