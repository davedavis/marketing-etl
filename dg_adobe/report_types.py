import json


def get_report_type(report_type, date_range):
    if report_type == 'revenue':
        report = get_revenue_report_type(date_range)

    elif report_type == 'conversion_rate':
        report = get_conversion_rate_report_type(date_range)

    else:
        print("You need to provide an Adobe report type like 'revenue' or 'conversion_rate.")
        report = None

    return report

# ToDo: Refactor hard coded paths.
def get_revenue_report_type(date_range):
    with open("./dg_adobe/adobe_revenue_by_day.json", "r") as content:
        gclid_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    # gclid_report_json_dict["globalFilters"][0]["dateRange"] = date_range
    report_request = json.dumps(gclid_report_json_dict)
    print("************** About to send Payload: {}".format(report_request))
    return report_request


def get_conversion_rate_report_type(date_range):
    with open("./dg_adobe/adobe_conversion_rate_by_day.json", "r") as content:
        gclid_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    # gclid_report_json_dict["globalFilters"][0]["dateRange"] = date_range
    report_request = json.dumps(gclid_report_json_dict)
    return report_request