import mysql
from suds import WebFault

from dg_microsoft.base_reports.auth import *
from bingads.v13.reporting import *


from dg_microsoft.base_reports.campaignmanagement_example_helper import output_status_message
from dg_microsoft.base_reports.output_helper import output_webfault_errors
from dg_db import storage
from dg_config import settingsfile
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter
from dg_utils.print_debug_headers import print_bing_qtd_accounts_headers

# Init settings
settings = settingsfile.get_settings()

# You must provide credentials in auth.py.
authorization_data = AuthorizationData(account_id=None,
                                       customer_id=None,
                                       developer_token=DEVELOPER_TOKEN,
                                       authentication=None,)

reporting_service_manager = ReportingServiceManager(authorization_data=authorization_data,
                                                    poll_interval_in_milliseconds=5000,
                                                    environment=ENVIRONMENT,)

# In addition to ReportingServiceManager, you will need a reporting ServiceClient to build the ReportRequest.
reporting_service = ServiceClient(service='ReportingService',
                                  version=13,
                                  authorization_data=authorization_data,
                                  environment=ENVIRONMENT,)


REPORT_FILE_FORMAT = settings['microsoft_report_format']

# The directory for the report files. Even though we're using the in memory object, the API still downloads a report.
FILE_DIRECTORY = settings['microsoft_file_directory']

# The name of the report download file.
RESULT_FILE_NAME = 'result.' + REPORT_FILE_FORMAT.lower()

# The maximum amount of time (in milliseconds) that you want to wait for the report download.
TIMEOUT_IN_MILLISECONDS = 3600000

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
microsoft_accounts = settings['microsoft_accounts']


# Set the download parameters and call the download_report method.
def build_microsoft_report_object(auth_data, start_date, end_date):
    """  Kick off the process of building the report object """
    print("Building report parameters...")
    try:
        report_request = build_microsoft_report_params(auth_data.account_id, start_date, end_date)

        reporting_params = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=FILE_DIRECTORY,
            result_file_name=RESULT_FILE_NAME,
            overwrite_result_file=True,
            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS
        )

        # Download the report in memory with ReportingServiceManager.download_report
        # The download_report helper function downloads the report and summarizes results.
        download_report(reporting_params)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)


# Downloads the report and gets an iterable report object.
def download_report(reporting_params):
    """ The download_report method returns both a file that will be downloaded and a report object. The report object
        can be gotten with the reporting_service_manager.download_report(reporting_download_parameters) method. Here,
        we're assigning it to a report_container variable and accessing the data from that."""

    print("Downloading the Microsoft Ads report...")

    # ToDo: Keep an eye on this and remove it completely.
    # global reporting_service_manager

    report_container = reporting_service_manager.download_report(reporting_params)

    if report_container is None:
        output_status_message("There is no report data for the submitted report request parameters.")
        sys.exit(0)

    report_record_iterable = report_container.report_records

    # Create a list to contain tuples from the response that we'll add to the database.
    records_to_insert = []

    # Print the headers for debugging in the console.
    print_bing_qtd_accounts_headers()

    for record in report_record_iterable:

        # Convert the date string into a datetime object, then convert it to the correct format in report spec.
        date_time_obj = datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')
        report_formatted_date = date_time_obj.strftime('%m/%d/%y')

        # Account Names contain the country, but are inconsistent. This is a simple function that
        # takes the account name and returns a clean country name.
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        # Print to the console for debugging.
        print(report_formatted_date,
              record.value('AccountNumber'),
              report_formatted_account_country,
              record.value('Impressions'),
              record.value('Clicks'),
              record.value('Spend'),
              week_number,
              sep='\t')

        # Convert each row to a tuple to be added to the DB.
        single_record_for_insertion = (record.value('TimePeriod'),
                                       record.value('AccountNumber'),
                                       report_formatted_account_country,
                                       record.value('Impressions'),
                                       record.value('Clicks'),
                                       record.value('Spend'),
                                       week_number)

        # Add the tuple to the list
        records_to_insert.append(single_record_for_insertion)

        # Get a DB object from the dg_db package storage connect method.
    try:
        connection = storage.connect()

        my_sql_insert_query = """INSERT INTO Bing_QTD_Account_Report (TimePeriod, AccountNumber, AccountName, Impressions, Clicks, Spend, Week)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        cursor.executemany(my_sql_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Bing_QTD_Account_Report table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    # Be sure to close the report.

    report_container.close()


def build_microsoft_report_params(account_id, start_date, end_date):
    """  Set the report object parameters. """

    aggregation = 'Daily'
    exclude_column_headers = False
    exclude_report_footer = False
    exclude_report_header = False

    # Create a ReportTime object and add the date as int values (currently receiving from main)
    time = reporting_service.factory.create('ReportTime')
    time.CustomDateRangeEnd.Day = end_date.day
    time.CustomDateRangeEnd.Month = end_date.month
    time.CustomDateRangeEnd.Year = end_date.year
    time.CustomDateRangeStart.Day = start_date.day
    time.CustomDateRangeStart.Month = start_date.month
    time.CustomDateRangeStart.Year = start_date.year

    time.ReportTimeZone = 'GreenwichMeanTimeDublinEdinburghLisbonLondon'

    return_only_complete_data = False

    complete_report_request_object = build_full_report(
        aggregation=aggregation,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time)

    return complete_report_request_object


# Define the actual report.
def build_full_report(aggregation, exclude_column_headers, exclude_report_footer, exclude_report_header, report_file_format, return_only_complete_data, time):

    """  Build the full report (Select your metrics and dimensions here) """

    report_request = reporting_service.factory.create('AccountPerformanceReportRequest')
    report_request.Aggregation = aggregation
    report_request.ExcludeColumnHeaders = exclude_column_headers
    report_request.ExcludeReportFooter = exclude_report_footer
    report_request.ExcludeReportHeader = exclude_report_header
    report_request.Format = report_file_format
    report_request.ReturnOnlyCompleteData = return_only_complete_data
    report_request.Time = time
    report_request.ReportName = "My Account Performance Report"
    scope = reporting_service.factory.create('AccountReportScope')
    scope.AccountIds = {'long': [microsoft_accounts]}
    report_request.Scope = scope

    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])
    report_request.Columns = report_columns

    return report_request


def get_campaign_report(start_date, end_date):
    start_date = start_date
    end_date = end_date
    authenticate(authorization_data)
    build_microsoft_report_object(authorization_data, start_date, end_date)
