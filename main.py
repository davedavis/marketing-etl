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
""" App that tracks the spend, revenue, E/R, Conversion Rate, CTR and percentage attainment in paid search by country
    and campaign type and generates"""
import argparse
import dg_microsoft
from dg_config.settingsfile import get_settings
from dg_date import daterange
from dg_microsoft import microsoft_ads_campaign_report


settings = get_settings()


def main(quarter):
    """ Main method that calls all the worker modules """
    print('Tracker Running...')
    print(f"Running for {quarter} quarter")

    # ToDo: Truncate and handle database stuff.

    # Set date range.
    if quarter == "this":
        google_date_range = daterange.google_thisq()
        bing_date_range_start = daterange.bing_thisq_start()
        bing_date_range_end = daterange.bing_thisq_end()
        print("Google Date Range is: ", google_date_range)
        print("Bing Date Range is: ", bing_date_range_start , bing_date_range_end)
    elif quarter == "last":
        google_date_range = daterange.google_lastq()
        bing_date_range_start = daterange.bing_lastq_start()
        bing_date_range_end = daterange.bing_lastq_end()
        print("Google Date Range is: ", google_date_range)
        print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)
    else:
        print("Sorry, reporting further back from last quarter is not supported yet, contact Dave if you need this.")

    # Get Microsoft Ads reports
    # ToDo: Implement using direct call to date range function (move into if statement)
    microsoft_ads_campaign_report.get_campaign_report(bing_date_range_start, bing_date_range_end)


if __name__ == "__main__":
    # Set up argparse and support reporting for previous quarter.
    parser = argparse.ArgumentParser(description="Updates or backfills SEM platform reporting.")
    parser.add_argument("-q", "--quarter",
                        type=str,
                        default="this",
                        help="The quarter you want the report for (this is default or last for backfill)")
    args = parser.parse_args()

    main(args.quarter)
