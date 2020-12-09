#  #!/usr/bin python

#  Copyright (c) 2020.  Dave Davis
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import mysql
from suds import WebFault

from dg_db.db_write import write_microsoft_report_to_db
from dg_microsoft.base_reports.auth import *
from bingads.v13.reporting import *

from dg_microsoft.base_reports.campaignmanagement_example_helper import output_status_message
from dg_microsoft.base_reports.output_helper import output_webfault_errors


from dg_config import settingsfile
from dg_microsoft.report_types import get_report_type


# Init settings
settings = settingsfile.get_settings()

# You must provide credentials in auth.py.
authorization_data = AuthorizationData(account_id=None,
                                       customer_id=None,
                                       developer_token=DEVELOPER_TOKEN,
                                       authentication=None, )

# Create a reporting service manager object.
reporting_service_manager = ReportingServiceManager(authorization_data=authorization_data,
                                                    poll_interval_in_milliseconds=5000,
                                                    environment=ENVIRONMENT, )

REPORT_FILE_FORMAT = settings['microsoft_report_format']

# Get list of Microsoft Advertising/Bing Advertising Accounts from the settings file.
microsoft_accounts = settings['microsoft_accounts']


# Set the download parameters and call the download_report method.
def build_microsoft_report_object(start_date, end_date, report_type):
    """  Kick off the process of building the report object """
    try:
        # Call, and get back a complete report type.
        report_request = get_report_type(report_type, start_date, end_date)

        report_download_request = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=settings['microsoft_file_directory'],
            result_file_name='result.' + REPORT_FILE_FORMAT.lower(),
            overwrite_result_file=settings['microsoft_report_overwrite_results_file'],
            timeout_in_milliseconds=settings['microsoft_report_timeout']
        )

        # Download the report in memory with ReportingServiceManager.download_report
        # The download_report helper function downloads the report and summarizes results.
        print(f"Downloading the Microsoft Ads {report_type} report...")

        report_container = reporting_service_manager.download_report(report_download_request)

        if report_container is None:
            output_status_message("There is no report data for the submitted report request parameters.")
            sys.exit(0)

        report_record_iterable = report_container.report_records

        # Return the report and send to the DB write module.
        return report_record_iterable

        # ToDo: Close the container

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)


# Main
def get_report(start_date, end_date, report_type):
    authenticate(authorization_data)
    records = build_microsoft_report_object(start_date, end_date, report_type)
    write_microsoft_report_to_db(records, report_type)
