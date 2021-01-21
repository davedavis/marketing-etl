import json


def get_report_type(report_type, date_range):
    if report_type == 'core_metrics':
        report = get_core_metrics_report_type(date_range)

    elif report_type == 'conversion_rate':
        report = get_conversion_rate_report_type(date_range)

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


def get_conversion_rate_report_type(date_range):
    with open("./dg_adobe/adobe_conversion_rate_by_day.json", "r") as content:
        gclid_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    # gclid_report_json_dict["globalFilters"][0]["dateRange"] = date_range
    report_request = json.dumps(gclid_report_json_dict)
    return report_request
