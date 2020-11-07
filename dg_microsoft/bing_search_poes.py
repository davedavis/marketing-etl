import mysql

from bing.base_reports.auth_helper import *
from bingads.v13.reporting import *

# You must provide credentials in auth.py.

# The report file extension type.
from bing.base_reports.campaignmanagement_example_helper import output_status_message
from bing.base_reports.output_helper import output_webfault_errors
from dg_db import storage, queries
from dg_utils import settingsfile
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter
from dg_utils.print_debug_headers import print_bing_search_poes_headers

authorization_data = AuthorizationData(
    account_id=None,
    customer_id=None,
    developer_token=DEVELOPER_TOKEN,
    authentication=None,
)

reporting_service_manager = ReportingServiceManager(
    authorization_data=authorization_data,
    poll_interval_in_milliseconds=5000,
    environment=ENVIRONMENT,
)

# In addition to ReportingServiceManager, you will need a reporting ServiceClient
# to build the ReportRequest.

reporting_service = ServiceClient(
    service='ReportingService',
    version=13,
    authorization_data=authorization_data,
    environment=ENVIRONMENT,
)

REPORT_FILE_FORMAT = 'Csv'

# The directory for the report files. Even though we're using the in memory object, the API still downloads a report.
FILE_DIRECTORY = 'bing/reports/'

# The name of the report download file.
RESULT_FILE_NAME = 'result.' + REPORT_FILE_FORMAT.lower()

# The maximum amount of time (in milliseconds) that you want to wait for the report download.
TIMEOUT_IN_MILLISECONDS = 3600000

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
settings = settingsfile.get_settings()
microsoft_accounts = settings['microsoft_accounts']


# Set the download parameters and call the download_report method.
def get_qtd_bing_poes(authorization_data, start_date, end_date):
    print("Attempting to get the Ads Report...")
    start_date = start_date
    end_date = end_date
    try:
        report_request = get_report_request(authorization_data.account_id, start_date, end_date)

        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=FILE_DIRECTORY,
            result_file_name=RESULT_FILE_NAME,
            overwrite_result_file=True,
            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS
        )

        # Download the report in memory with ReportingServiceManager.download_report
        # The download_report helper function downloads the report and summarizes results.
        download_report(reporting_download_parameters)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)


# Downloads the report and gets an iterable report object.
def download_report(reporting_download_parameters):
    """ The download_report method returns both a file that will be downloaded and a report object. The report object
        can be gotten with the reporting_service_manager.download_report(reporting_download_parameters) method. Here,
        we're assigning it to a report_container variable and accessing the data from that."""

    global reporting_service_manager

    report_container = reporting_service_manager.download_report(reporting_download_parameters)

    if report_container is None:
        output_status_message("There is no report data for the submitted report request parameters.")
        sys.exit(0)

    report_record_iterable = report_container.report_records

    # Create a list to contain tuples from the response that we'll add to the database.
    records_to_insert = []

    # Print the headers for the console. Will be removed in DB.
    print_bing_search_poes_headers()

    for record in report_record_iterable:

        # This converts the date string received back from Google into a datetime object and passes it to
        # The get_week_in_quarter to get the week number for custom reporting.
        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        # Filter out no cost data rows
        if record.value('Spend') != '0.00':
            # Print to the console for debugging.

            # Using a try except block for this as some records come back with weird CTR values like ('') that can't be
            # Converted into a float. So we catch the exception and keep going, just not adding the exception into
            # the DB.
            try:
                report_formatted_ctr = float(record.value('Ctr').strip('%')) / 100.0

                # Account Names contain the country, but are inconsistent. This is a simple function that
                # takes the account name and returns a clean country name.
                report_formatted_account_country = clean_country_name(record.value('AccountName'))

                print(record.value('TimePeriod'),
                      week_number,
                      'Microsoft',
                      'Not Available',
                      report_formatted_account_country,
                      record.value('CampaignName'),
                      record.value('CurrencyCode'),
                      record.value('Spend'),
                      record.value('Impressions'),
                      record.value('Clicks'),
                      report_formatted_ctr,  # CTR
                      record.value('AverageCpc'),
                      'Search',
                      '',
                      record.value('TitlePart1'),
                      record.value('TitlePart2'),
                      record.value('TitlePart3'),
                      record.value('AdDescription'),
                      record.value('AdDescription2'),
                      record.value('Path1'),
                      record.value('Path2'),
                      '',
                      '',
                      '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '',
                      sep='\t')

                # Convert each row to a tuple to be added to the DB.
                single_record_for_insertion = (record.value('TimePeriod'),
                                               week_number,
                                               'Microsoft',
                                               'Not Available',
                                               report_formatted_account_country,
                                               record.value('CampaignName'),
                                               record.value('CurrencyCode'),
                                               record.value('Spend'),
                                               record.value('Impressions'),
                                               record.value('Clicks'),
                                               report_formatted_ctr,  # CTR
                                               record.value('AverageCpc'),
                                               'Search',
                                               '',
                                               record.value('TitlePart1'),
                                               record.value('TitlePart2'),
                                               record.value('TitlePart3'),
                                               record.value('AdDescription'),
                                               record.value('AdDescription2'),
                                               record.value('Path1'),
                                               record.value('Path2'),
                                               '',
                                               '',
                                               '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                               '', '', '', ''
                                               )

                # Add the tuple to the list
                records_to_insert.append(single_record_for_insertion)

            except ValueError as e:
                print(e)
                print("There was a problem with a row")
                print("The CTR Value trying to be parsed is : ", record.value('Ctr'))

        # Get a DB object from the dg_db package storage connect method.
    try:
        connection = storage.poe_connect()
        query = queries.get_poe_query()

        cursor = connection.cursor()
        cursor.executemany(query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into rt_poes table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    # Be sure to close the report.

    report_container.close()


def get_report_request(account_id, start_date, end_date):
    """
    Use a sample report request or build your own.
    """

    aggregation = 'Daily'
    exclude_column_headers = False
    exclude_report_footer = True
    exclude_report_header = True

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

    account_performance_report_request = get_account_performance_report_request(
        account_id=account_id,
        aggregation=aggregation,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time)

    return account_performance_report_request


# Define the actual report.
def get_account_performance_report_request(
        account_id,
        aggregation,
        exclude_column_headers,
        exclude_report_footer,
        exclude_report_header,
        report_file_format,
        return_only_complete_data,
        time):
    report_request = reporting_service.factory.create('AdPerformanceReportRequest')
    report_request.Aggregation = aggregation
    report_request.ExcludeColumnHeaders = exclude_column_headers
    report_request.ExcludeReportFooter = exclude_report_footer
    report_request.ExcludeReportHeader = exclude_report_header
    report_request.Format = report_file_format
    report_request.ReturnOnlyCompleteData = return_only_complete_data
    report_request.Time = time
    report_request.ReportName = "Bing-Microsoft Ads POE Report"
    scope = reporting_service.factory.create('AccountThroughAdGroupReportScope')
    # scope.AccountIds = {'long': [account_id]}
    scope.AccountIds = {'long': [microsoft_accounts]}
    report_request.Scope = scope

    report_columns = reporting_service.factory.create('ArrayOfAdPerformanceReportColumn')
    report_columns.AdPerformanceReportColumn.append([
        'TimePeriod',
        'AccountName',
        'CampaignName',
        'AdGroupName',
        'CurrencyCode',
        'AdDistribution',
        'Impressions',
        'Clicks',
        'Ctr',
        'AverageCpc',
        'Spend',
        'AdGroupId',
        'AdTitle',
        'AdDescription',
        'AdDescription2',
        'AdType',
        'TitlePart1',
        'TitlePart2',
        'TitlePart3',
        'Path1',
        'Path2'
    ])

    report_request.Columns = report_columns

    return report_request


def get_bing_search_poes(start_date, end_date):
    start_date = start_date
    end_date = end_date
    authenticate(authorization_data)
    get_qtd_bing_poes(authorization_data, start_date, end_date)
