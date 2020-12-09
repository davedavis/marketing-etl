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
""" App that pulls account reports, campaign reports, and ads reports from both Google and Bing and stores them in
    a database for report generation"""
import argparse
import time
from tqdm import tqdm as tqdm

from dg_config.settingsfile import get_settings
from dg_date import daterange
from dg_db.db_utils import init_db
from dg_google import google_ads_report_builder
from dg_microsoft import microsoft_ads_report_builder

settings = get_settings()


def main(quarter):
    """ Main method that calls all the worker modules """
    print('Tracker Running...')
    print(f"Running for {quarter} quarter")

    # For timing the running of the app.
    t0 = time.time()
    print('App runtime timer started...')

    # Truncate and setup database tables with SQLAlchemy
    print('Truncating database tables...')
    init_db()
    print('Tables truncated.')

    # Set date range.
    print('Calculating date range for reports..')
    if quarter == "this":
        google_date_range = daterange.google_thisq()
        bing_date_range_start = daterange.bing_thisq_start()
        bing_date_range_end = daterange.bing_thisq_end()
        print("Google Date Range is: ", google_date_range)
        print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)
    elif quarter == "last":
        google_date_range = daterange.google_lastq()
        bing_date_range_start = daterange.bing_lastq_start()
        bing_date_range_end = daterange.bing_lastq_end()
        print("Google Date Range is: ", google_date_range)
        print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)
    else:
        print("Sorry, reporting further back from last quarter is not supported yet, contact Dave if you need this.")

    # Initialize the report retrieval flow. Stagger platforms & sleep for rate limiting.
    google_ads_report_builder.get_report(google_date_range, report_type="accounts")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="accounts")
    time.sleep(10)

    google_ads_report_builder.get_report(google_date_range, report_type="campaigns")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="campaigns")
    time.sleep(10)

    google_ads_report_builder.get_report(google_date_range, report_type="ads")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="ads")
    time.sleep(10)

    google_ads_report_builder.get_report(google_date_range, report_type="shopping")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="shopping")

    # End of the app run, calculate the total time it took.
    print("Time to get all the reports and write them all to the database today is "
          + str(time.time() - t0)[:-15] + " secs. Or " + str((time.time() - t0) / 60)[:-15] + " minutes.")


if __name__ == "__main__":
    # Set up argparse and support reporting for previous quarter.
    parser = argparse.ArgumentParser(description="Updates or backfills SEM platform reporting.")
    parser.add_argument("-q", "--quarter",
                        type=str,
                        default="this",
                        help="The quarter you want the report for ('this' is default or 'last' for backfill)")
    args = parser.parse_args()

    main(args.quarter)
    # main('last')
