#  #!/usr/bin python

"""Paid media and analytics ETL pipeline.
   Pulls report data from Google Ads, Microsoft Ads as well as metrics and dimensions from Adobe Analytics.
   Creates models for accounts, platforms and fiscal business week/quarters and creates relationships between
   these and the the report models. Once data is extracted and transformed, it's loaded into a database for
   much easier querying and report building.

   All settings and info on each can be found in the settings.yaml file and all are required.
"""

# Leave this import for convenient app execution timing. It is actually used.
from time import sleep

import dg_utils.timing

from dg_adobe import adobe_report_builder
from dg_config.settingsfile import get_settings
from dg_date import daterange
from dg_db.db_utils import init_db
from dg_db.populate import populate_accounts, populate_skews, populate_platforms
from dg_google import google_ads_report_builder
from dg_microsoft import microsoft_ads_report_builder
from rich.console import Console

console = Console()
settings = get_settings()


def main(quarter, year):
    """Gets the reports from platforms and writes them to the appropriate
       DB tables in the database defined in the settings.yaml file.

    Args:
        quarter (int): The fiscal quarter the reports should be pulled for.
        year (str): The fiscal year the reports should be pulled for. "last" otherwise "this".

    """

    console.print('Tracker Running...')
    console.print(f"Running for quarter {quarter} ")

    # Truncate and setup database tables with SQLAlchemy
    console.print('Checking database integrity...')
    init_db(quarter, year)

    # # ToDo: Implement if exists and if start of quarter.
    # # Database initialization with seed data.
    # Seed Countries to DB
    # populate_accounts()
    # # Seed Platforms to DB
    # populate_platforms()
    # Get the Skews
    # populate_skews()

    # Set date range.
    console.print('Calculating date range for reports..')
    google_date_range = daterange.get_google_date_range(quarter, year)
    bing_date_range_start, bing_date_range_end = daterange.get_bing_date_range(quarter, year)
    adobe_full_date_range = daterange.get_adobe_date_range(quarter, year)

    console.print("Google Date Range is: ", google_date_range)
    console.print("Bing Date Range is: ", bing_date_range_start, bing_date_range_end)
    console.print("Adobe Date Range is: ", adobe_full_date_range)

    # Initialize the report retrieval flow. Stagger & sleep for rate limiting.
    # Start the Accounts report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="accounts")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="accounts")

    # Start the Campaigns report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="campaigns")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="campaigns")

    # Start the Search Ads report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="ads")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="ads")

    # Start the Shopping Ads report flow for all platforms.
    google_ads_report_builder.get_report(google_date_range, report_type="shopping")
    microsoft_ads_report_builder.get_report(bing_date_range_start, bing_date_range_end, report_type="shopping")

    # Start the Adobe Revenue report flow.
    adobe_report_builder.get_report(adobe_full_date_range, report_type="emea_metrics")

    # Start the Budget Cap report flow.
    # ToDo: Check for status = PAUSED
    google_ads_report_builder.get_report(google_date_range, report_type="budgetcap")


if __name__ == "__main__":
    main(2, "this")

