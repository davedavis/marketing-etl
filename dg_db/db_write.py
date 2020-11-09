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

import mysql

from dg_config import settingsfile
from dg_db import storage
# Init settings
settings = settingsfile.get_settings()
connection = storage.connect()

def write_microsoft_campaign_report(report_results):

    try:

        my_sql_insert_query = """INSERT INTO Bing_QTD_Account_Report (TimePeriod, AccountNumber, AccountName, Impressions, Clicks, Spend, Week)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        cursor.executemany(my_sql_insert_query, report_results)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Bing_QTD_Account_Report table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
