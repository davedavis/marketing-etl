import mysql
from suds import WebFault

from dg_db.db_write import write_microsoft_campaign_report
from dg_microsoft.base_reports.auth import *
from bingads.v13.reporting import *

from dg_microsoft.base_reports.campaignmanagement_example_helper import output_status_message
from dg_microsoft.base_reports.output_helper import output_webfault_errors
from dg_db import storage
from dg_config import settingsfile
from dg_microsoft.report_types import get_report_type
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter
from dg_utils.print_debug_headers import print_bing_qtd_accounts_headers

# Init settings
settings = settingsfile.get_settings()

# You must provide credentials in auth.py.
authorization_data = AuthorizationData(account_id=None, customer_id=None, developer_token=DEVELOPER_TOKEN,
                                       authentication=None, )

# Create a reporting service manager object.
reporting_service_manager = ReportingServiceManager(authorization_data=authorization_data,
                                                    poll_interval_in_milliseconds=5000, environment=ENVIRONMENT, )

REPORT_FILE_FORMAT = settings['microsoft_report_format']

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
microsoft_accounts = settings['microsoft_accounts']


# Set the download parameters and call the download_report method.
def build_microsoft_report_object(start_date, end_date, report_type):
    """  Kick off the process of building the report object """
    try:
        # Call, and get back a complete report request.
        report_request = get_report_type(report_type, start_date, end_date)

        report_download_request = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=settings['microsoft_file_directory'],
            result_file_name='result.' + REPORT_FILE_FORMAT.lower(),
            overwrite_result_file=settings['microsoft_report_overwrite_results_file'],
            timeout_in_milliseconds=settings['microsoft_report_timeout']
        )

        # Download the report in memory with ReportingServiceManager.download_report
        # The download_report helper function downloads the report and summarizes results.
        download_report(report_download_request)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)


# Downloads the report and gets an iterable report object.
def download_report(report_download_request):
    """ The download_report method returns both a file that will be downloaded and a report object. The report object
        can be gotten with the reporting_service_manager.download_report(reporting_download_parameters) method. Here,
        we're assigning it to a report_container variable and accessing the data from that."""

    print("Downloading the Microsoft Ads report...")

    # ToDo: Keep an eye on this and remove it completely.
    # global reporting_service_manager

    report_container = reporting_service_manager.download_report(report_download_request)

    if report_container is None:
        output_status_message("There is no report data for the submitted report request parameters.")
        sys.exit(0)

    report_record_iterable = report_container.report_records

    # Create a list to contain tuples from the response that we'll add to the database.
    records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_record_iterable:
        # Convert the date string into a datetime object, then convert it to the correct format in report spec.
        date_time_obj = datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')
        report_formatted_date = date_time_obj.strftime('%m/%d/%y')

        # Account Names contain the country, but are inconsistent. This is a simple function that
        # takes the account name and returns a clean country name.
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        print(report_formatted_date, report_formatted_account_country, record.value('Spend'), week_number)

        # # Print to the console for debugging.
        # print(report_formatted_date,
        #       record.value('AccountNumber'),
        #       report_formatted_account_country,
        #       record.value('Impressions'),
        #       record.value('Clicks'),
        #       record.value('Spend'),
        #       week_number,
        #       sep='\t')
        #
        # # Convert each row to a tuple to be added to the DB.
        # single_record_for_insertion = (record.value('TimePeriod'),
        #                                record.value('AccountNumber'),
        #                                report_formatted_account_country,
        #                                record.value('Impressions'),
        #                                record.value('Clicks'),
        #                                record.value('Spend'),
        #                                week_number)

        # Add the tuple to the list
        # records_to_insert.append(single_record_for_insertion)

    # Write to DB using the DB module.
    write_microsoft_campaign_report(records_to_insert)

    # Be sure to close the report.
    report_container.close()


# Main
def get_report(start_date, end_date, report_type):
    authenticate(authorization_data)
    build_microsoft_report_object(start_date, end_date, report_type)
