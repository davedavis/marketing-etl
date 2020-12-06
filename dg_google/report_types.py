def get_report_type(report_type, date_range):
    if report_type == 'accounts':
        report = get_account_report_type(date_range)

    elif report_type == 'campaigns':
        report = get_campaign_report_type(date_range)

    elif report_type == 'ads':
        report = get_search_ads_report_type(date_range)

    else:
        print("You need to provide a report type like 'accounts', 'campaigns' or 'ads'.")
        report = None

    return report


def get_account_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions
                         FROM customer 
                         WHERE segments.date 
                         BETWEEN {date_range}'''
    return report_request


def get_campaign_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, segments.date, metrics.cost_micros, metrics.clicks
                         FROM customer 
                         WHERE segments.date 
                         BETWEEN {date_range}'''
    return report_request


def get_search_ads_report_type(date_range):
    report_request = f'''SELECT customer.descriptive_name, segments.date, metrics.cost_micros, metrics.clicks
                         FROM customer 
                         WHERE segments.date 
                         BETWEEN {date_range}'''

    return report_request
