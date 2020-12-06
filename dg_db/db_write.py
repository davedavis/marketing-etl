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

# Import DB utils
from dg_db.db_utils import get_session
# Import models
from dg_models.accounts_report_model import AccountReportRecord
from dg_models.campaigns_report_model import CampaignReportRecord
from dg_models.ads_report_model import AdReportRecord

# Import Settings
from dg_config import settingsfile

# Import helper functions
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter

# Init settings
settings = settingsfile.get_settings()


def write_google_report_to_db(report_results, report_type):
    if report_type == 'accounts':
        write_google_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_google_campaigns_report(report_results)

    elif report_type == 'ads':
        write_google_ads_report(report_results)

    else:
        print("You need to provide a report type like 'accounts', 'campaigns' or 'ads'.")


def write_microsoft_report_to_db(report_results, report_type):
    if report_type == 'accounts':
        write_microsoft_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_microsoft_campaigns_report(report_results)

    elif report_type == 'ads':
        write_microsoft_ads_report(report_results)

    else:
        print("You need to provide a report type like 'accounts', 'campaigns' or 'ads'.")


def write_google_accounts_report(report_results):
    print("Google Accounts report received, writing to DB")

    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_formatted_account_country = clean_country_name(record.customer.descriptive_name)
        week_number = get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d"))
        account_number = record.customer.resource_name.split("/")[1]

        report_record = AccountReportRecord(platform="Google",
                                            account_name=report_formatted_account_country,
                                            account_number=account_number,
                                            time_period=record.segments.date,
                                            week=week_number,
                                            impressions=record.metrics.impressions,
                                            clicks=record.metrics.clicks,
                                            spend=record.metrics.cost_micros / 1000000)

        # session.add(report_record)
        accounts_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(accounts_report_records_to_insert)
    # Commit the session
    session.commit()


def write_microsoft_accounts_report(report_results):
    print("Microsoft Accounts report received, writing to DB")
    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        # Account Names contain the country, but are inconsistent. This is a simple function that
        # takes the account name and returns a clean country name. ToDo: Move this into Model.
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        # Set the week number based off the time period field.
        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        report_record = AccountReportRecord(platform='Microsoft',
                                            account_name=report_formatted_account_country,
                                            account_number=record.value('AccountNumber'),
                                            time_period=record.value('TimePeriod'),
                                            week=week_number,
                                            impressions=record.value('Impressions'),
                                            clicks=record.value('Clicks'),
                                            spend=record.value('Spend'))

        # session.add(report_record)
        accounts_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(accounts_report_records_to_insert)
    # Commit the session
    session.commit()

    # ToDo: Evaluate if this needs to be done.
    # session.close()


def write_google_campaigns_report(report_results):
    print("Campaigns report received, writing to DB")
    campaigns_report_records_to_insert = []

    for record in report_results:
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        report_record = CampaignReportRecord(platform='Microsoft',
                                             account_name=report_formatted_account_country,
                                             account_number=record.value('AccountNumber'),
                                             time_period=record.value('TimePeriod'),
                                             week=week_number,
                                             campaign=record.value('CampaignName'),
                                             campaign_id=record.value('CampaignId'),
                                             network=record.value('Network'),
                                             impressions=record.value('Impressions'),
                                             clicks=record.value('Clicks'),
                                             spend=record.value('Spend'))

        campaigns_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(campaigns_report_records_to_insert)
    session.commit()


def write_microsoft_campaigns_report(report_results):
    print("Microsoft Campaigns report received, writing to DB")
    campaigns_report_records_to_insert = []

    for record in report_results:
        report_formatted_account_country = clean_country_name(record.value('AccountName'))

        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        report_record = CampaignReportRecord(platform='Microsoft',
                                             account_name=report_formatted_account_country,
                                             account_number=record.value('AccountNumber'),
                                             time_period=record.value('TimePeriod'),
                                             week=week_number,
                                             campaign=record.value('CampaignName'),
                                             campaign_id=record.value('CampaignId'),
                                             network=record.value('Network'),
                                             impressions=record.value('Impressions'),
                                             clicks=record.value('Clicks'),
                                             spend=record.value('Spend'))

        campaigns_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(campaigns_report_records_to_insert)
    session.commit()


def write_google_ads_report(report_results):
    print("Ads report received, writing to DB")
    ads_report_records_to_insert = []

    for record in report_results:
        report_formatted_account_country = clean_country_name(record.value('AccountName'))
        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        # Check and make sure an empty string wasn't received. Bing... I want to strangle you!
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        report_record = AdReportRecord(platform='Microsoft',
                                       account_name=report_formatted_account_country,
                                       account_number=record.value('AccountNumber'),
                                       time_period=record.value('TimePeriod'),
                                       week=week_number,
                                       campaign=record.value('CampaignName'),
                                       currency=record.value('CampaignId'),
                                       impressions=record.value('Impressions'),
                                       clicks=record.value('Clicks'),
                                       spend=record.value('Spend'),
                                       ctr=report_formatted_ctr,
                                       average_cpc=record.value('AverageCpc'),
                                       headline_1=record.value('TitlePart1'),
                                       ad_type='Search',
                                       headline_2=record.value('TitlePart2'),
                                       headline_3=record.value('TitlePart3'),
                                       description_1=record.value('AdDescription'),
                                       description_2=record.value('AdDescription2'),
                                       path_1=record.value('Path1'),
                                       path_2=record.value('Path2'),
                                       )

        ads_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(ads_report_records_to_insert)
    session.commit()


def write_microsoft_ads_report(report_results):
    print("Microsoft Ads report received, writing to DB")
    ads_report_records_to_insert = []

    for record in report_results:
        report_formatted_account_country = clean_country_name(record.value('AccountName'))
        week_number = get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d'))

        # Check and make sure an empty string wasn't received. Bing... I want to strangle you!
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        report_record = AdReportRecord(platform='Microsoft',
                                       account_name=report_formatted_account_country,
                                       account_number=record.value('AccountNumber'),
                                       time_period=record.value('TimePeriod'),
                                       week=week_number,
                                       campaign=record.value('CampaignName'),
                                       currency=record.value('CampaignId'),
                                       impressions=record.value('Impressions'),
                                       clicks=record.value('Clicks'),
                                       spend=record.value('Spend'),
                                       ctr=report_formatted_ctr,
                                       average_cpc=record.value('AverageCpc'),
                                       headline_1=record.value('TitlePart1'),
                                       ad_type='Search',
                                       headline_2=record.value('TitlePart2'),
                                       headline_3=record.value('TitlePart3'),
                                       description_1=record.value('AdDescription'),
                                       description_2=record.value('AdDescription2'),
                                       path_1=record.value('Path1'),
                                       path_2=record.value('Path2'),
                                       )

        ads_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(ads_report_records_to_insert)
    session.commit()
