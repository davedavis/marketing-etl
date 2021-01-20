import configparser
import datetime
import json
import logging
import os
from time import sleep
import requests



def get_gclid_report(config, global_company_id, access_token, adobe_date, rsid):
    with open("config/report_definition.json", "r") as content:
        gclid_report_json_dict = json.load(content)
    # Set the adobe date in the dictionary.
    gclid_report_json_dict["globalFilters"][0]["dateRange"] = adobe_date
    gclid_report_json_dict["rsid"] = rsid
    gclid_report_json_string = json.dumps(gclid_report_json_dict)
    logger.info("Sending Payload: {}".format(gclid_report_json_string))
    response = requests.post(
        "{}/{}/reports".format(config["analyticsapiurl"], global_company_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
            'x-api-key': config["apikey"],
            'x-proxy-global-company-id': global_company_id,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=gclid_report_json_string
    )
    if response.json() is not None:
        return response.json()


def date_range_generator(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


# Method that takes the data returned from the Adobe API and prints it with some additional info to the console.
def print_filtered_response():
    global row, hour_dollar_value
    if 'rows' in day_response:
        for row in day_response["rows"]:
            # Begin filtering out the needed data from the response.
            if row["value"] != "Unspecified" or "(Low Traffic)":
                # Map list/array indexes to hours + 1 hour to ensure revenue is assigned an hour later.
                for hour_dollar_value in row["data"]:
                    if hour_dollar_value != 0.0:
                        print(row["value"], "\t",
                              "EMEA Imported Conversions", "\t",
                              current_date.strftime("%m-%d-%Y") + " " + str(row["data"].index(hour_dollar_value)) + ":00",
                              "\t",
                              round(hour_dollar_value, 2), "\t",
                              "USD")



# Method that calls the Adobe reporting API and get's back the gclid evar by hour each day.
def get_gclids_from_report_suites():
    global current_rsid, day_response, current_date
    # For each rsid
    for rsid in rsids:
        # sleep(20)
        # Set up the weird required Adobe date format. e.g, 2020-04-01T00:00:00.000/2020-04-02T00:00:00.000
        adobe_report_format_daily_delta = current_date + datetime.timedelta(seconds=86400)
        adobe_delta = adobe_report_format_daily_delta.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        adobe_date = current_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "/" + adobe_delta
        google_date = current_date.strftime("%m-%d-%Y %H:%M:%S")
        current_rsid = rsid

        # Create a date range iterable and call the report on each date in the date range.
        for id, single_date in enumerate(date_range_generator(start_date, end_date)):
            day_response = get_gclid_report(config, global_company_id, access_token, adobe_date, current_rsid)
            logger.info(day_response)
            if day_response is not None:
                # Print the response to the console and write the response to a CSV file.
                print_filtered_response()
                open_write_csv_file()

                # Increment the adobe date.
                current_date = single_date + datetime.timedelta(days=1)
                adobe_report_format_daily_delta = current_date + datetime.timedelta(seconds=86400)
                adobe_delta = adobe_report_format_daily_delta.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                adobe_date = current_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "/" + adobe_delta
                # Set a delay. The Adobe API will only allow 300 requests a minute PER RSID.
                # sleep(20)
        # Reset the current date for each new RSID iteration back to the start date.
        current_date = start_date


def main():

    # Remove existing gclids file if it exists.
    gclid_file = ('gclids.csv')
    if os.path.exists(gclid_file):
        os.remove(gclid_file)
        print('Old gclid file deleted. Ready to rock.')
    else:
        print("Can not delete the gclid file as it's already gone. All good.")

    global logger, config, access_token, global_company_id, start_date, end_date, current_date, rsids, current_rsid
    # Set up logger and config parser.
    logging.basicConfig(level="INFO")
    logger = logging.getLogger()

    config_parser = configparser.ConfigParser()
    config_parser.read('config/config.ini')
    config = dict(config_parser["default"])

    # Get JWT token and store access token for reporting API requests.
    jwt_token = get_jwt_token(config)
    logger.info("JWT Token: {}".format(jwt_token))
    access_token = get_access_token(config, jwt_token)
    logger.info("Access Token: {}".format(access_token))
    global_company_id = get_first_global_company_id(config, access_token)
    logger.info("global_company_id: {}".format(global_company_id))

    # Set the date range for the report.
    # start_date = datetime.date(2020, 9, 7)
    # end_date = datetime.date(2020, 9, 22)

    start_date = datetime.date.today() - datetime.timedelta(days=7)
    end_date = datetime.date.today()

    current_date = start_date

    # Get a list of RSIDs this report is to be run on and set the first one.
    rsids = json.loads(config['rsids'])
    current_rsid = rsids[0]

    # Call the function that gets the gclids.
    get_gclids_from_report_suites()
