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
from dg_models.account_model import Account
from dg_models.accounts_report_model import AccountReportRecord
from dg_models.campaigns_report_model import CampaignReportRecord
from dg_models.ads_report_model import AdReportRecord

# Import Settings
from dg_config import settingsfile
from rich.console import Console

from dg_models.skew_model import Skew

console = Console()

# Import helper functions
from dg_models.core_metrics_report_model import MetricsReportRecord
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter

# Init settings
from dg_utils.region_converter import get_region

settings = settingsfile.get_settings()


def write_google_report_to_db(report_results, report_type):
    console.print(f"Google {report_type} report received, writing to DB...")

    if report_type == 'accounts':
        write_google_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_google_campaigns_report(report_results)

    elif report_type == 'ads':
        write_google_search_ads_report(report_results)

    elif report_type == 'shopping':
        write_google_shopping_ads_report(report_results)

    else:
        console.print("You need to provide a Google Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping.")


def write_adobe_report_to_db(report_results, report_type):
    console.print(f"Adobe {report_type} report received, writing to DB...")

    if report_type == 'core_metrics':
        write_adobe_core_metrics_report(report_results)

    elif report_type == 'emea_metrics':
        write_adobe_emea_metrics_report(report_results)

    else:
        console.print("You need to provide an report type like 'revenue' or 'conversion_rate.")


def write_skews(skews):
    skews_to_insert = []


    # Loop through the returned records and do something with them.
    for record in skews:
        session = get_session()
        country_fk = session.query(Account.id).filter_by(account_country_code=record[0]).first().id
        session.close()


        skew = Skew(
                    account=country_fk,
                    quarter=record[1],
                    week=record[2],
                    spend_target=record[3],
                    revenue_target=record[4],
                    er_target=record[5],

                   )

        skews_to_insert.append(skew)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(skews_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print("All Skews added to DB")


def write_countries(countries):
    countries_to_insert = []

    # Loop through the returned records and do something with them.
    for country in countries:
        country_record = Account(account_name=country[0],
                                 account_country_code=country[1],
                                 account_region=country[2],
                                 account_subregion=country[3],
                                 )

        # session.add(report_record)
        countries_to_insert.append(country_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(countries_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print("All Countries added to DB")






def write_adobe_core_metrics_report(report_results):
    # Create a list to contain tuples from the response that we'll add to the database.
    metrics_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_record = MetricsReportRecord(account_name=clean_country_name(record[1]),
                                            account_region=get_region(record[1]),
                                            time_period=record[0],
                                            week=get_week_in_quarter(record[0]),
                                            revenue=record[2],
                                            conversion_rate=record[3] * 100,
                                            visits=record[4],
                                            orders=record[5],
                                            aov=record[6],
                                            units=record[7],
                                            aur=record[8])

        # session.add(report_record)
        metrics_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(metrics_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print("All Adobe Records added to DB")


def write_adobe_emea_metrics_report(report_results):
    # Create a list to contain tuples from the response that we'll add to the database.
    metrics_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:

        ## Convert the string date returned to a datetime object
        record_date = datetime.strptime(record[1], '%b %d, %Y')

        report_record = MetricsReportRecord(account_name=clean_country_name(record[0]),
                                            account_region=get_region(record[0]),
                                            time_period=record_date.date(),
                                            week=get_week_in_quarter(record_date),
                                            revenue=record[2],
                                            conversion_rate=record[3] * 100,
                                            visits=record[4],
                                            orders=record[5],
                                            aov=record[6],
                                            units=record[7],
                                            aur=record[8])

        # session.add(report_record)
        metrics_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(metrics_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print("All Adobe Records added to DB")


def write_microsoft_report_to_db(report_results, report_type):
    console.print(f"Microsoft {report_type} report received, writing to DB...")

    if report_type == 'accounts':
        write_microsoft_accounts_report(report_results)

    elif report_type == 'campaigns':
        write_microsoft_campaigns_report(report_results)

    elif report_type == 'ads':
        write_microsoft_search_ads_report(report_results)

    elif report_type == 'shopping':
        write_microsoft_shopping_ads_report(report_results)

    else:
        console.print("You need to provide a Microsoft Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping'.")


def write_google_accounts_report(report_results):
    # For timing the DB writes. Compare at the end of the method.
    tga = time.time()

    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_record = AccountReportRecord(platform="Google",
                                            account_name=clean_country_name(record.customer.descriptive_name),
                                            account_region=get_region(record.customer.descriptive_name),
                                            account_number=record.customer.resource_name.split("/")[1],
                                            time_period=record.segments.date,
                                            week=get_week_in_quarter(
                                                datetime.strptime(record.segments.date, "%Y-%m-%d")),
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

    console.print("Total time for adding Google accounts to the database was " + str(time.time() - tga)[:-15] + " secs ")


def write_google_campaigns_report(report_results):
    tgc = time.time()
    campaigns_report_records_to_insert = []

    for record in report_results:
        # Get the channel ENUM from the client so we can see the specific network the ad was run on.
        # Search, Shopping, Display, Display Select etc.
        channel = GoogleAdsClient.get_type('AdvertisingChannelTypeEnum')

        report_record = CampaignReportRecord(platform="Google",
                                             account_name=clean_country_name(record.customer.descriptive_name),
                                             account_number=record.customer.resource_name.split("/")[1],
                                             time_period=record.segments.date,
                                             week=get_week_in_quarter(
                                                 datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                             campaign=record.campaign.name,
                                             campaign_id=record.campaign.id,
                                             network=channel.AdvertisingChannelType.Name(
                                                 record.campaign.advertising_channel_type).title(),
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

    console.print("Total time for adding Google campaigns to the database was " + str(time.time() - tgc)[:-15] + " secs ")


def write_google_search_ads_report(report_results):
    tgsa = time.time()
    ads_report_records_to_insert = []

    for record in report_results:
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

        # Get the channel ENUM from the client so we can see the specific network the ad was run on.
        # Search, Shopping, Display, Display Select etc.
        channel = GoogleAdsClient.get_type('AdvertisingChannelTypeEnum')

        # Switch descriptions for DSAs and normal ETAs
        if record.ad_group_ad.ad.expanded_dynamic_search_ad.description:
            description1 = record.ad_group_ad.ad.expanded_dynamic_search_ad.description
        else:
            description1 = record.ad_group_ad.ad.expanded_text_ad.description

        if record.ad_group_ad.ad.expanded_dynamic_search_ad.description2:
            description2 = record.ad_group_ad.ad.expanded_dynamic_search_ad.description2
        else:
            description2 = record.ad_group_ad.ad.expanded_text_ad.description2

        # Build the record for insertion.
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
                                       path_1=record.ad_group_ad.ad.expanded_text_ad.path1,
                                       path_2=record.ad_group_ad.ad.expanded_text_ad.path2,
                                       headline_1=record.ad_group_ad.ad.expanded_text_ad.headline_part1,
                                       headline_2=record.ad_group_ad.ad.expanded_text_ad.headline_part2,
                                       headline_3=record.ad_group_ad.ad.expanded_text_ad.headline_part3,
                                       description_1=description1,
                                       description_2=description2,
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

    console.print("Total time for adding Google search ads to the database was " + str(time.time() - tgsa)[:-15] + " secs ")


def write_google_shopping_ads_report(report_results):
    tgshop = time.time()
    shopping_ads_report_records_to_insert = []

    for record in report_results:
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

    console.print("Total time for adding Google shopping ads to the database was " + str(time.time() - tgshop)[:-15] + " secs ")


def write_microsoft_accounts_report(report_results):
    tma = time.time()

    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_record = AccountReportRecord(platform='Microsoft',
                                            account_name=clean_country_name(record.value('AccountName')),
                                            account_region=get_region(record.value('AccountName')),
                                            account_number=record.value('AccountNumber'),
                                            time_period=record.value('TimePeriod'),
                                            week=get_week_in_quarter(
                                                datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
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

    console.print("Total time for adding Microsoft accounts to the database was " + str(time.time() - tma)[:-15] + " secs ")


def write_microsoft_campaigns_report(report_results):
    tmc = time.time()

    campaigns_report_records_to_insert = []

    for record in report_results:
        report_record = CampaignReportRecord(platform='Microsoft',
                                             account_name=clean_country_name(record.value('AccountName')),
                                             account_number=record.value('AccountNumber'),
                                             time_period=record.value('TimePeriod'),
                                             week=get_week_in_quarter(
                                                 datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
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

    console.print("Total time for adding Microsoft campaigns to the database was " + str(time.time() - tmc)[:-15] + " secs ")


def write_microsoft_search_ads_report(report_results):
    tmsa = time.time()

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
                                       week=get_week_in_quarter(
                                           datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
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

    console.print("Total time for adding Microsoft ads to the database was " + str(time.time() - tmsa)[:-15] + " secs ")


def write_microsoft_shopping_ads_report(report_results):
    tmshop = time.time()

    ads_report_records_to_insert = []

    for record in report_results:
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        report_record = AdReportRecord(platform='Microsoft',
                                       account_name=clean_country_name(record.value('AccountName')),
                                       account_number=record.value('AccountNumber'),
                                       time_period=record.value('TimePeriod'),
                                       week=get_week_in_quarter(
                                           datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
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

    console.print("Total time for adding Microsoft shopping ads to the database was " + str(time.time() - tmshop)[
                                                                                :-15] + " secs ")
