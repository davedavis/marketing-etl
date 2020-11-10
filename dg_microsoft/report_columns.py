from dg_microsoft.microsoft_ads_report_builder import reporting_service


def get_account_report_columns():
    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])


def get_campaign_report_columns():
    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])


def get_ads_report_columns():
    report_columns = reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'TimePeriod',
        'AccountNumber',
        'AccountName',
        'Impressions',
        'Clicks',
        'Spend'
    ])

