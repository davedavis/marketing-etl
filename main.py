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

"""Paid media platform report pulling pipeline.

This script pulls data from Google Ads, Microsoft Ads and Adobe Analytics
And writes it to a custom database for later report generation.
It is assumed that this will be run from the command line with the quarter
passed as an argument. As the database tables are determined by these
parameters, this script will not work in an IDE.

This script requires that `SQLAlchemy` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:
    * main - the main function of the script
"""

# Leave this import for app execution timing.
import sys

import dg_utils.timing

# This module is required for custom quarter and weeks based on company fiscal year.
import fiscalyear
import argparse

from dg_adobe import adobe_report_builder
from dg_config.settingsfile import get_settings
from dg_date import daterange
from dg_db.db_utils import init_db
from dg_google import google_ads_report_builder
from dg_microsoft import microsoft_ads_report_builder
from rich.console import Console

console = Console()
settings = get_settings()


def main(quarter):
    """Gets the reports from platforms and writes them to the appropriate
       DB tables in the database defined in the settings.yaml file.

    Args:
        quarter (int): The fiscal quarter the reports should be pulled for.

    """

    console.print('Tracker Running...')
    console.print(f"Running for quarter {quarter} ")

    # Truncate and setup database tables with SQLAlchemy
    console.print('Truncating database tables...')
    # ToDo: Truncate individual tables at component/report runtime, not all at once.
    init_db()
    console.print('Tables truncated.')

    # Set date range.
    console.print('Calculating date range for reports..')
    google_date_range = daterange.get_google_date_range(quarter)
    bing_date_range_start, bing_date_range_end = daterange.get_bing_date_range(quarter)
    adobe_date_range_start, adobe_date_range_end = daterange.get_adobe_date_range(quarter)

    console.print("Google Date Range is: ", google_date_range)
    console.print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)
    console.print("Adobe Date Range is: ", adobe_date_range_start, adobe_date_range_end)

    # # Initialize the report retrieval flow. Stagger platforms & sleep for rate limiting.
    # # Start the Accounts report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="accounts")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="accounts")
    #
    # # Start the Campaigns report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="campaigns")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="campaigns")
    #
    # # Start the Search Ads report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="ads")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="ads")
    #
    # # Start the Shopping Ads report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="shopping")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="shopping")

    # Start the Adobe Revenue report flow.
    adobe_report_builder.get_report(adobe_date_range_start, adobe_date_range_end, report_type="core_metrics")
    # adobe_report_builder.get_report(adobe_date_range, report_type="conversion_rate")

# ToDo: Change country/region converter into single function.
# ToDo: Make args a global variable instead of accessing them directly in the model for dynamic table creation.
if __name__ == "__main__":
    # Set up argparse and support reporting for previous quarter.
    parser = argparse.ArgumentParser(description="Updates or backfills database with SEM platform reporting.")
    parser.add_argument("-q", "--quarter",
                        type=int,
                        default=fiscalyear.FiscalQuarter.current().quarter,
                        help="The quarter as an integer. 1, 2, 3 or 4 which will be for the current fiscal year.")
    args = parser.parse_args()

    main(args.quarter)
