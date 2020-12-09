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
import time
from datetime import datetime
from tqdm import tqdm as tqdm

# Import DB utils
from google.ads.google_ads.client import GoogleAdsClient

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
    print(f"Google {report_type} report received, writing to DB...")

    if report_type == 'accounts':
        write_google_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_google_campaigns_report(report_results)

    elif report_type == 'ads':
        write_google_search_ads_report(report_results)

    elif report_type == 'shopping':
        write_google_shopping_ads_report(report_results)

    else:
        print("You need to provide a Google Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping.")


def write_microsoft_report_to_db(report_results, report_type):
    print(f"Microsoft {report_type} report received, writing to DB...")

    if report_type == 'accounts':
        write_microsoft_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_microsoft_campaigns_report(report_results)

    elif report_type == 'ads':
        write_microsoft_search_ads_report(report_results)

    elif report_type == 'shopping':
        write_microsoft_shopping_ads_report(report_results)

    else:
        print("You need to provide a Microsoft Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping'.")


def write_google_accounts_report(report_results):
    # For timing the DB writes. Compare at the end of the method.
    t0 = time.time()

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
    # Close the session
    session.close()

    print("Total time for adding Google accounts to the database was " + str(time.time() - t0) + " secs ")


def write_google_campaigns_report(report_results):
    t0 = time.time()
    campaigns_report_records_to_insert = []

    for record in report_results:
        report_formatted_account_country = clean_country_name(record.customer.descriptive_name)
        week_number = get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d"))
        account_number = record.customer.resource_name.split("/")[1]

        # Get the channel ENUM from the client so we can see the specific network the ad was run on.
        # Search, Shopping, Display, Display Select etc.
        channel = GoogleAdsClient.get_type('AdvertisingChannelTypeEnum')
        network = channel.AdvertisingChannelType.Name(record.campaign.advertising_channel_type).title()

        report_record = CampaignReportRecord(platform="Google",
                                             account_name=report_formatted_account_country,
                                             account_number=account_number,
                                             time_period=record.segments.date,
                                             week=week_number,
                                             campaign=record.campaign.name,
                                             campaign_id=record.campaign.id,
                                             network=network,
                                             impressions=record.metrics.impressions,
                                             clicks=record.metrics.clicks,
                                             spend=record.metrics.cost_micros / 1000000)

        # session.add(report_record)
        campaigns_report_records_to_insert.append(report_record)

        # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(campaigns_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    print("Total time for adding Google campaigns to the database was " + str(time.time() - t0) + " secs ")


def write_google_search_ads_report(report_results):
    t0 = time.time()
    ads_report_records_to_insert = []

    for record in report_results:
        # print(record)

        # Handle RSA ad types first as SQLAlchemy needs to insert uniform objects..
        # Create a list for each of the RSA asset sets that comes back. Initialize to empty string for uniformity.
        rsa_headline_list = [''] * 15
        rsa_description_list = [''] * 4

        # Then check if the ad is a responsive search ad.
        if record.ad_group_ad.ad.responsive_search_ad.headlines:
            # Handle the RSAs as they come back as containers with iterable string items.
            # Loop through the iterable and assign the string to the position in the initialized list.
            for headline_pos, rsa_headline in enumerate(record.ad_group_ad.ad.responsive_search_ad.headlines):
                rsa_headline_list[headline_pos] = rsa_headline.text

            # # Same as above for the descriptions.
            for description_pos, rsa_description in enumerate(record.ad_group_ad.ad.responsive_search_ad.descriptions):
                rsa_description_list[description_pos] = rsa_description.text

        # Some formatting for the DB and some additional field calculations.
        report_formatted_account_country = clean_country_name(record.customer.descriptive_name)
        week_number = get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d"))
        account_number = record.customer.resource_name.split("/")[1]
        report_formatted_ctr = record.metrics.ctr * 100
        report_formatted_average_cpc = record.metrics.average_cpc / 1000000

        # Get the channel ENUM from the client so we can see the specific network the ad was run on.
        # Search, Shopping, Display, Display Select etc.
        channel = GoogleAdsClient.get_type('AdvertisingChannelTypeEnum')

        # Build the record for insertion.
        report_record = AdReportRecord(platform='Google',
                                       account_name=report_formatted_account_country,
                                       account_number=account_number,
                                       time_period=record.segments.date,
                                       week=week_number,
                                       campaign=record.campaign.name,
                                       currency=record.customer.currency_code,
                                       impressions=record.metrics.impressions,
                                       clicks=record.metrics.clicks,
                                       spend=record.metrics.cost_micros / 1000000,
                                       ctr=report_formatted_ctr,
                                       average_cpc=report_formatted_average_cpc,
                                       ad_type=channel.AdvertisingChannelType.Name(
                                           record.campaign.advertising_channel_type).title(),
                                       path_1=record.ad_group_ad.ad.expanded_text_ad.path1,
                                       path_2=record.ad_group_ad.ad.expanded_text_ad.path2,
                                       headline_1=record.ad_group_ad.ad.expanded_text_ad.headline_part1,
                                       headline_2=record.ad_group_ad.ad.expanded_text_ad.headline_part2,
                                       headline_3=record.ad_group_ad.ad.expanded_text_ad.headline_part3,
                                       description_1=record.ad_group_ad.ad.expanded_dynamic_search_ad.description,
                                       description_2=record.ad_group_ad.ad.expanded_dynamic_search_ad.description2,
                                       rsa_headline_1=rsa_headline_list[0],
                                       rsa_headline_2=rsa_headline_list[1],
                                       rsa_headline_3=rsa_headline_list[2],
                                       rsa_headline_4=rsa_headline_list[3],
                                       rsa_headline_5=rsa_headline_list[4],
                                       rsa_headline_6=rsa_headline_list[5],
                                       rsa_headline_7=rsa_headline_list[6],
                                       rsa_headline_8=rsa_headline_list[7],
                                       rsa_headline_9=rsa_headline_list[8],
                                       rsa_headline_10=rsa_headline_list[9],
                                       rsa_headline_11=rsa_headline_list[10],
                                       rsa_headline_12=rsa_headline_list[11],
                                       rsa_headline_13=rsa_headline_list[12],
                                       rsa_headline_14=rsa_headline_list[13],
                                       rsa_headline_15=rsa_headline_list[14],
                                       rsa_description_1=rsa_description_list[0],
                                       rsa_description_2=rsa_description_list[1],
                                       rsa_description_3=rsa_description_list[2],
                                       rsa_description_4=rsa_description_list[3],
                                       )

        ads_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(ads_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    print("Total time for adding Google search ads to the database was " + str(time.time() - t0) + " secs ")


def write_google_shopping_ads_report(report_results):
    t0 = time.time()
    shopping_ads_report_records_to_insert = []

    for record in report_results:
        # ToDo: Clean up report formatted values. Add directly into parameters.
        # report_formatted_account_country = clean_country_name(record.customer.descriptive_name)
        # week_number = get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d"))
        account_number = record.customer.resource_name.split("/")[1]
        report_formatted_ctr = record.metrics.ctr * 100
        report_formatted_average_cpc = record.metrics.average_cpc / 1000000

        # Get the channel ENUM from the client so we can see the specific network the ad was run on.
        # Search, Shopping, Display, Display Select etc.
        channel = GoogleAdsClient.get_type('AdvertisingChannelTypeEnum')

        report_record = AdReportRecord(platform='Google',
                                       account_name=clean_country_name(record.customer.descriptive_name),
                                       account_number=record.customer.resource_name.split("/")[1],
                                       time_period=record.segments.date,
                                       week=get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                       campaign=record.campaign.name,
                                       currency=record.customer.currency_code,
                                       impressions=record.metrics.impressions,
                                       clicks=record.metrics.clicks,
                                       spend=record.metrics.cost_micros / 1000000,
                                       ctr=record.metrics.ctr * 100,
                                       average_cpc=record.metrics.average_cpc / 1000000,
                                       ad_type=channel.AdvertisingChannelType.Name(
                                           record.campaign.advertising_channel_type).title(),
                                       shopping_title=record.segments.product_title
                                       )

        # session.add(report_record)
        shopping_ads_report_records_to_insert.append(report_record)

        # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(shopping_ads_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    print("Total time for adding Google shopping ads to the database was " + str(time.time() - t0) + " secs ")


def write_microsoft_accounts_report(report_results):
    t0 = time.time()

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
    # Close the session
    session.close()

    print("Total time for adding Microsoft accounts to the database was " + str(time.time() - t0) + " secs ")


def write_microsoft_campaigns_report(report_results):
    t0 = time.time()

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
    # Close the session
    session.close()

    print("Total time for adding Microsoft campaigns to the database was " + str(time.time() - t0) + " secs ")


def write_microsoft_search_ads_report(report_results):
    t0 = time.time()

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
                                       currency='USD',
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
    # Close the session
    session.close()

    print("Total time for adding Microsoft ads to the database was " + str(time.time() - t0) + " secs ")


def write_microsoft_shopping_ads_report(report_results):
    t0 = time.time()

    ads_report_records_to_insert = []

    for record in report_results:
        # Check and make sure an empty string wasn't received. Bing... I want to strangle you!
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        report_record = AdReportRecord(platform='Microsoft',
                                       account_name=clean_country_name(record.value('AccountName')),
                                       account_number=record.value('AccountNumber'),
                                       time_period=record.value('TimePeriod'),
                                       week=get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
                                       campaign=record.value('CampaignName'),
                                       currency=record.value('CurrencyCode'),
                                       impressions=record.value('Impressions'),
                                       clicks=record.value('Clicks'),
                                       spend=record.value('Spend'),
                                       ctr=report_formatted_ctr,
                                       average_cpc=record.value('AverageCpc'),
                                       ad_type='Shopping',
                                       shopping_title=record.value('Title')
                                       )

        ads_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(ads_report_records_to_insert)
    session.commit()
    session.close()

    print("Total time for adding Microsoft shopping ads to the database was " + str(time.time() - t0) + " secs ")
