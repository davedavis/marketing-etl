import mysql
from suds import WebFault

from dg_db.db_write import write_microsoft_campaign_report
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
authorization_data = AuthorizationData(account_id=None, customer_id=None, developer_token=DEVELOPER_TOKEN,
                                       authentication=None, )

# Create a reporting service manager object.
reporting_service_manager = ReportingServiceManager(authorization_data=authorization_data,
                                                    poll_interval_in_milliseconds=5000, environment=ENVIRONMENT, )

# In addition to ReportingServiceManager, you will need a reporting ServiceClient to build the ReportRequest.
reporting_service = ServiceClient(service='ReportingService', version=13, authorization_data=authorization_data,
                                  environment=ENVIRONMENT, )

REPORT_FILE_FORMAT = settings['microsoft_report_format']

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
microsoft_accounts = settings['microsoft_accounts']


# Set the download parameters and call the download_report method.
def build_microsoft_report_object(auth_data, start_date, end_date):
    """  Kick off the process of building the report object """
    print("Building report parameters...")
    try:

        # Create a ReportTime object and add the date as int values (currently receiving from main)
        report_time = reporting_service.factory.create('ReportTime')
        report_time.CustomDateRangeEnd.Day = end_date.day
        report_time.CustomDateRangeEnd.Month = end_date.month
        report_time.CustomDateRangeEnd.Year = end_date.year
        report_time.CustomDateRangeStart.Day = start_date.day
        report_time.CustomDateRangeStart.Month = start_date.month
        report_time.CustomDateRangeStart.Year = start_date.year
        report_time.ReportTimeZone = settings['microsoft_report_timezone']

        report_request = reporting_service.factory.create('AccountPerformanceReportRequest')
        report_request.Aggregation = settings['microsoft_report_aggregation']
        report_request.ExcludeColumnHeaders = settings['microsoft_report_exclude_column_headers']
        report_request.ExcludeReportFooter = settings['microsoft_report_exclude_report_footer']
        report_request.ExcludeReportHeader = settings['microsoft_report_exclude_report_header']
        report_request.Format = REPORT_FILE_FORMAT
        report_request.ReturnOnlyCompleteData = settings['microsoft_report_return_only_complete_data']
        report_request.Time = report_time
        report_request.ReportName = "My Account Performance Report"
        scope = reporting_service.factory.create('AccountReportScope')
        scope.AccountIds = {'long': [microsoft_accounts]}
        report_request.Scope = scope


        #############################################################################################
        #                               Parameterize                                                #
        #############################################################################################

        # ToDo: pass in report columns from main

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

        # reporting_service_factory_object
        # report_column

        #############################################################################################
        #                               Parameterize                                                #
        #############################################################################################

        complete_report_object = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=settings['microsoft_file_directory'],
            result_file_name='result.' + REPORT_FILE_FORMAT.lower(),
            overwrite_result_file=settings['microsoft_report_overwrite_results_file'],
            timeout_in_milliseconds=settings['microsoft_report_timeout']
        )

        # Download the report in memory with ReportingServiceManager.download_report
        # The download_report helper function downloads the report and summarizes results.
        download_report(complete_report_object)

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

    # Write to DB using the DB module.
    write_microsoft_campaign_report(records_to_insert)

    # Be sure to close the report.
    report_container.close()


# Main
def get_report(start_date, end_date):
    start_date = start_date
    end_date = end_date
    authenticate(authorization_data)
    build_microsoft_report_object(authorization_data, start_date, end_date)
