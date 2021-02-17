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


def get_report(date_range_start, date_range_end, report_type):
    # Authenticate
    access_token, global_company_id = adobe_analytics_auth()

    # Adobe has weird report date range requirements with odd formatting. It
    # also doesn't allow the day dimension to be labeled, so it's easier to
    # just call the report for each day in the date range rather than get the
    # entire date range with an unlabeled date day dimension (positional in a
    # list) So... Split out the daterange into separate days and add them to
    # a list.
    day_list = pd.date_range(date_range_start, date_range_end - datetime.timedelta(days=1), freq='d')

    # Container for returned records.
    records_to_insert = []

    for day in day_list:
        end_of_day = day + datetime.timedelta(hours=24)
        report_date = day.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "/" + end_of_day.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        # Get the report type and query string.
        query = get_report_type(report_type, report_date)

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


                    cleaned_record = [day.to_pydatetime(), record["value"], record["data"][0],
                                      record["data"][1], record["data"][2], record["data"][3],
                                      record["data"][4], record["data"][5], record["data"][6]]

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
    write_adobe_report_to_db(records_to_insert, report_type)
