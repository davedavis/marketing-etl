import json


def get_report_type(report_type, date_range, rsid):
    if report_type == 'core_metrics':
        report = get_core_metrics_report_type(date_range)

    elif report_type == 'emea_metrics':
        report = get_country_metrics_report_type(date_range, rsid)

    else:
        print("You need to provide an Adobe report type like 'revenue' or 'conversion_rate.")
        report = None

    return report


# ToDo: Refactor hard coded paths.
def get_core_metrics_report_type(date_range):
    # Load the report into a dict to easily change the date range.
    with open("./dg_adobe/adobe_analytics_metrics_by_day.json", "r") as content:
        adobe_analytics_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    adobe_analytics_report_json_dict["globalFilters"][3]["dateRange"] = date_range
    report_request = json.dumps(adobe_analytics_report_json_dict)
    return report_request


def get_country_metrics_report_type(date_range, rsid):
    # Load the report into a dict to easily change the date range.
    with open("./dg_adobe/adobe_analytics_metrics_by_day_rsid.json", "r") as content:
        adobe_analytics_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    adobe_analytics_report_json_dict["globalFilters"][4]["dateRange"] = date_range
    adobe_analytics_report_json_dict["rsid"] = rsid
    report_request = json.dumps(adobe_analytics_report_json_dict)
    return report_request
