from bingads import ServiceClient, AuthorizationData

from dg_config import settingsfile
from dg_microsoft.base_reports.auth import ENVIRONMENT, DEVELOPER_TOKEN

settings = settingsfile.get_settings()
REPORT_FILE_FORMAT = settings['microsoft_report_format']

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
microsoft_accounts = settings['microsoft_accounts']

# You must provide credentials in auth.py.
authorization_data = AuthorizationData(account_id=None, customer_id=None, developer_token=DEVELOPER_TOKEN,
                                       authentication=None, )

# In addition to ReportingServiceManager, you will need a reporting ServiceClient to build the ReportRequest.
reporting_service = ServiceClient(service='ReportingService', version=13, authorization_data=authorization_data,
                                  environment=ENVIRONMENT, )


def get_report_type(report_type, start_date, end_date):

    if report_type == 'account':
        report = get_account_report_type(start_date, end_date)

    elif report_type == 'campaign':
        report = get_campaign_report_type()

    elif report_type == 'ads':
        report = get_ads_report_type()

    else:
        report = None

    return report


def get_account_report_type(start_date, end_date):
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


def get_campaign_report_type():
    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])

    return report_columns


def get_ads_report_type():
    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])

    return report_columns
