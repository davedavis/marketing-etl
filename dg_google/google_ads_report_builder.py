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

# Init settings
import sys
from tqdm import tqdm as tqdm

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

from dg_config import settingsfile
from dg_config.settingsfile import get_settings_file_path
from dg_db.db_write import write_google_report_to_db
from dg_google.report_types import get_report_type

settings = settingsfile.get_settings()


def get_report(date_range, report_type):
    google_ads_client = GoogleAdsClient.load_from_storage(get_settings_file_path())
    ga_service = google_ads_client.get_service('GoogleAdsService', version='v6')
    print(f"Fetching the Google Ads {report_type} reports...")
    query = get_report_type(report_type, date_range)

    records_to_insert = []

    for account in tqdm(settings['google_accounts'], position=0, leave=True):
        response = ga_service.search_stream(str(account), query)

        # Get the data from the API
        try:
            for batch in response:
                for row in batch.results:
                    records_to_insert.append(row)

        # Boilerplate exception code.
        except GoogleAdsException as ex:
            print(f'Request with the ID "{ex.request_id}" failed with the status '
                  f'"{ex.error.code().name}" and includes the below errors:')
            for error in ex.failure.errors:
                print(f'\tError with the message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f'\t\tOn the field: {field_path_element.field_name}')
            sys.exit(1)

    print(f"Google {report_type} report received, writing to DB...")

    write_google_report_to_db(records_to_insert, report_type)
