#  #!/usr/bin python
#  Copyright (c) 2020.  Dave Davis
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      https://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime
import pandas as pd

# Links :
# https://stackoverflow.com/questions/2877410/python-store-a-dict-in-a-database
#

import mysql
from pandas import DataFrame

from dg_config import settingsfile
from dg_db import storage

# Init settings
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter

settings = settingsfile.get_settings()
connection = storage.connect()


def write_microsoft_report_to_db(report_results, report_type):

    if report_type == 'accounts':
        write_microsoft_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_microsoft_campaigns_report(report_results)

    elif report_type == 'ads':
        write_microsoft_ads_report(report_results)

    else:
        print("You need to provide a report type like 'accounts', 'campaigns' or 'ads'.")


def write_microsoft_accounts_report(report_results):
    # Create a list to contain tuples from the response that we'll add to the database.
    records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        # Convert the date string into a datetime object, then convert it to the correct format in report spec.
        date_time_obj = datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')
        report_formatted_date = date_time_obj.strftime('%m/%d/%y')

        # Account Names contain the country, but are inconsistent. This is a simple function that
        # takes the account name and returns a clean country name.
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        # Set the week number based off the time period field.
        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        # Print the returned report to the screen for debugging.
        # print(record._row_values.columns)

        # Convert each row to a tuple to be added to the DB.
        single_record_for_insertion = (report_formatted_date,
                                       record.value('AccountNumber'),
                                       report_formatted_account_country,
                                       record.value('Impressions'),
                                       record.value('Clicks'),
                                       record.value('Spend'),
                                       week_number)
        print(single_record_for_insertion)

        # Add the tuple to the list
        records_to_insert.append(single_record_for_insertion)

    try:

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


def write_microsoft_campaigns_report(report_results):
    pass


def write_microsoft_ads_report(report_results):
    pass
