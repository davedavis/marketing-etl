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

# Import DB utils
from functools import reduce


from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from dg_db.db_utils import get_session
# Import models
from dg_models.account_model import Account
from dg_models.accounts_report_model import AccountReportRecord
from dg_models.budget_recommendation_model import BudgetRecommendation
from dg_models.campaigns_report_model import CampaignReportRecord
from dg_models.ads_report_model import AdReportRecord

# Import Settings
from dg_config import settingsfile
from rich.console import Console

from dg_models.platform_model import Platform
from dg_models.skew_model import Skew
from dg_utils.quarter_utils import get_quarter_from_date

console = Console()

# Import helper functions
from dg_models.analytics_model import MetricsReportRecord
from dg_utils.clean_country import clean_country_name
from dg_utils.get_quarter_week import get_week_in_quarter

# Init settings
from dg_utils.region_converter import get_region

settings = settingsfile.get_settings()


def get_foreign_keys(table_name):
    # Get the foreign Keys for all Accounts as we can't insert with a query on a foreign key using
    # SQLAlchemy bulk insert.
    account_fk_dict = {}
    google_platform_fk_dict = {}
    microsoft_platform_fk_dict = {}
    session = get_session()

    if table_name == "accounts":
        accounts = session.query(Account.id, Account.account_name).all()
        for account in accounts:
            account_fk_dict.update({account.account_name: account.id})
        return account_fk_dict

    elif table_name == "google_platforms":
        google_platforms = session.query(Platform.id, Platform.account).filter_by(platform="Google").all()
        for platform in google_platforms:
            google_platform_fk_dict.update({platform.account: platform.id})
        return google_platform_fk_dict


    elif table_name == "microsoft_platforms":
        microsoft_platforms = session.query(Platform.id, Platform.account).filter_by(platform="Microsoft").all()
        for platform in microsoft_platforms:
            microsoft_platform_fk_dict.update({platform.account: platform.id})
        return microsoft_platform_fk_dict

    session.close()


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

    elif report_type == 'budgetcap':
        write_budget_recommendation_report(report_results)

    else:
        console.print("You need to provide a Google Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping.")


def write_adobe_report_to_db(report_results, report_type):
    console.print(f"Adobe {report_type} report received, writing to DB...")

    if report_type == 'emea_metrics':
        write_adobe_emea_metrics_report(report_results)

    else:
        console.print("You need to provide an report type like 'revenue' or 'conversion_rate.")


def write_platforms(platforms):
    platforms_to_insert = []

    # Loop through the returned records and do something with them.
    for record in platforms:
        platform = Platform(
            account=record[0],
            platform=record[1],
            account_number=record[2],
            new_account_number=record[3],
        )

        platforms_to_insert.append(platform)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(platforms_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print("All Platforms added to DB")


def write_skews(skews):
    skews_to_insert = []

    # Loop through the returned records and do something with them.
    for record in skews:
        # To get the foreign key, we need to open and close a session.
        # ToDo: Query once and store all account IDs in a dict.
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


def write_adobe_emea_metrics_report(report_results):
    # Create a list to contain tuples from the response that we'll add to the database.
    metrics_report_records_to_insert = []

    account_fks = get_foreign_keys("accounts")

    # Loop through the returned records and do something with them.
    for record in report_results:
        ## Convert the string date returned to a datetime object
        record_date = datetime.strptime(record[1], '%b %d, %Y')

        report_record = MetricsReportRecord(account=account_fks.get(clean_country_name(record[0])),
                                            date=record_date.date(),
                                            week=get_week_in_quarter(record_date),
                                            quarter=get_quarter_from_date(record_date),
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
        console.print(
            "You need to provide a Microsoft Ads report type like 'accounts', 'campaigns', 'ads' or 'shopping'.")


def write_google_accounts_report(report_results):
    # For timing the DB writes. Compare at the end of the method.
    tga = time.time()

    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    google_platform_fks = get_foreign_keys("google_platforms")

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_record = AccountReportRecord(
            account=account_fks.get(clean_country_name(record.customer.descriptive_name)),
            platform=google_platform_fks.get(account_fks.get(clean_country_name(record.customer.descriptive_name))),
            date=record.segments.date,
            week=get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d")),
            quarter=get_quarter_from_date(datetime.strptime(record.segments.date, "%Y-%m-%d")),
            impressions=record.metrics.impressions,
            clicks=record.metrics.clicks,
            spend=(record.metrics.cost_micros / 1000000) / settings['exchange_rate']
        )

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

    console.print(
        "Total time for adding Google accounts to the database was " + str(time.time() - tga)[:-15] + " secs ")


def write_google_campaigns_report(report_results):
    tgc = time.time()
    campaigns_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    google_platform_fks = get_foreign_keys("google_platforms")




    for record in report_results:
        report_record = CampaignReportRecord(
            account=account_fks.get(clean_country_name(record.customer.descriptive_name)),
            platform=google_platform_fks.get(account_fks.get(clean_country_name(record.customer.descriptive_name))),
            status=record.campaign.status.name,
            date=record.segments.date,
            week=get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d")),
            quarter=get_quarter_from_date(datetime.strptime(record.segments.date, "%Y-%m-%d")),
            campaign_name=record.campaign.name,
            campaign_id=record.campaign.id,
            network=record.campaign.advertising_channel_type.name,
            impressions=record.metrics.impressions,
            clicks=record.metrics.clicks,
            spend=(record.metrics.cost_micros / 1000000) / settings['exchange_rate'],
            conversions=record.metrics.conversions,
            cost_per_conversion=(record.metrics.cost_per_conversion / 1000000) / settings['exchange_rate'],
            value_per_conversion=(record.metrics.value_per_conversion) * settings['exchange_rate'],
            conversion_value=(record.metrics.conversions_value) * settings['exchange_rate'],
            conversion_rate=record.metrics.conversions_from_interactions_rate,
            conversion_value_per_cost=(record.metrics.conversions_value * settings['exchange_rate']) / ((record.metrics.cost_micros * 1000000) / settings['exchange_rate']),
            impression_share=record.metrics.search_impression_share,
            budget_lost_is=record.metrics.search_budget_lost_impression_share,
            rank_lost_is=record.metrics.search_rank_lost_impression_share
        )

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

    console.print(
        "Total time for adding Google campaigns to the database was " + str(time.time() - tgc)[:-15] + " secs ")


def write_google_search_ads_report(report_results):
    tgsa = time.time()
    ads_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    google_platform_fks = get_foreign_keys("google_platforms")

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
        report_record = AdReportRecord(account=account_fks.get(clean_country_name(record.customer.descriptive_name)),
                                       platform=google_platform_fks.get(
                                           account_fks.get(clean_country_name(record.customer.descriptive_name))),
                                       date=record.segments.date,
                                       week=get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                       quarter=get_quarter_from_date(
                                           datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                       campaign=record.campaign.name,
                                       currency=record.customer.currency_code,
                                       impressions=record.metrics.impressions,
                                       clicks=record.metrics.clicks,
                                       spend=(record.metrics.cost_micros / 1000000) / settings['exchange_rate'],
                                       ctr=record.metrics.ctr * 100,
                                       average_cpc=(record.metrics.average_cpc / 1000000) / settings['exchange_rate'],
                                       ad_type=record.campaign.advertising_channel_type.name,
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

    console.print(
        "Total time for adding Google search ads to the database was " + str(time.time() - tgsa)[:-15] + " secs ")


def write_google_shopping_ads_report(report_results):
    tgshop = time.time()
    shopping_ads_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    google_platform_fks = get_foreign_keys("google_platforms")

    for record in report_results:

        report_record = AdReportRecord(account=account_fks.get(clean_country_name(record.customer.descriptive_name)),
                                       platform=google_platform_fks.get(
                                           account_fks.get(clean_country_name(record.customer.descriptive_name))),
                                       date=record.segments.date,
                                       week=get_week_in_quarter(datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                       quarter=get_quarter_from_date(
                                           datetime.strptime(record.segments.date, "%Y-%m-%d")),
                                       campaign=record.campaign.name,
                                       currency=record.customer.currency_code,
                                       impressions=record.metrics.impressions,
                                       clicks=record.metrics.clicks,
                                       spend=(record.metrics.cost_micros / 1000000) / settings['exchange_rate'],
                                       ctr=record.metrics.ctr * 100,
                                       average_cpc=record.metrics.average_cpc / 1000000,
                                       ad_type=record.campaign.advertising_channel_type.name,
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

    console.print(
        "Total time for adding Google shopping ads to the database was " + str(time.time() - tgshop)[:-14] + " secs ")


def write_budget_recommendation_report(report_results):
    brr = time.time()
    # Budget Recommendations come back from the API with a daily dimension which is not very useful
    # as there are multiple duplicates/entries for the same campaign, showing the same recommendation
    # for each date. What we want is to show only one recommendation fo each campaign. So we pull the
    # the records, then deduplicate.

    # Loop through the report results and add all entries, including duplicates to a list
    recommendation_dict_list = []
    for row in report_results:
        temp_dict = {}
        temp_dict['Account'] = row.customer.descriptive_name
        temp_dict['Campaign ID'] = row.campaign.id
        temp_dict['Campaign Name'] = row.campaign.name
        temp_dict['Current Budget'] = row.campaign_budget.amount_micros / 1000000
        temp_dict['Recommended Budget'] = row.campaign_budget.recommended_budget_amount_micros / 1000000
        recommendation_dict_list.append(temp_dict)

    # Use a Lambda function to remove duplicates
    unique_recommendations = reduce(lambda l, x: l.append(x) or l if x not in l else l, recommendation_dict_list, [])

    # Then add the unique list to the DB as normal.
    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    google_platform_fks = get_foreign_keys("google_platforms")

    # Create a list to hold the BudgetRecommendation objects.
    budget_recommendation_records_to_insert = []

    for record in unique_recommendations:
        report_record = BudgetRecommendation(
            account=account_fks.get(clean_country_name(record['Account'])),
            platform=google_platform_fks.get(account_fks.get(clean_country_name(record['Account']))),
            campaign_id=record['Campaign ID'],
            campaign_name=record['Campaign Name'],
            current_budget=record['Current Budget'],
            recommended_budget=record['Recommended Budget'],

        )

        # session.add(report_record)
        budget_recommendation_records_to_insert.append(report_record)

        # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(budget_recommendation_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print(f"{len(budget_recommendation_records_to_insert)} budget recommendations were retrieved.")
    console.print(
        "Total time for adding Budget Recommendations to the database was " + str(time.time() - brr)[:-14] + " secs ")


def write_microsoft_accounts_report(report_results):
    tma = time.time()

    # Create a list to contain tuples from the response that we'll add to the database.
    accounts_report_records_to_insert = []

    account_fks = get_foreign_keys("accounts")
    microsoft_platform_fks = get_foreign_keys("microsoft_platforms")

    # Loop through the returned records and do something with them.
    for record in report_results:
        report_record = AccountReportRecord(
            account=account_fks.get(clean_country_name(record.value('AccountName'))),
            platform=microsoft_platform_fks.get(account_fks.get(clean_country_name(record.value('AccountName')))),
            date=record.value('TimePeriod'),
            week=get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
            quarter=get_quarter_from_date(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
            impressions=record.value('Impressions'),
            clicks=record.value('Clicks'),
            spend=float(record.value('Spend')) / settings['exchange_rate']
        )

        accounts_report_records_to_insert.append(report_record)

    # Set up DB session
    session = get_session()
    # Bulk save the records from the list
    session.bulk_save_objects(accounts_report_records_to_insert)
    # Commit the session
    session.commit()
    # Close the session
    session.close()

    console.print(
        "Total time for adding Microsoft accounts to the database was " + str(time.time() - tma)[:-15] + " secs ")


def write_microsoft_campaigns_report(report_results):
    tmc = time.time()

    campaigns_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    microsoft_platform_fks = get_foreign_keys("microsoft_platforms")

    for record in report_results:
        report_record = CampaignReportRecord(
            account=account_fks.get(clean_country_name(record.value('AccountName'))),
            platform=microsoft_platform_fks.get(account_fks.get(clean_country_name(record.value('AccountName')))),
            status=record.value('CampaignStatus'),
            date=record.value('TimePeriod'),
            week=get_week_in_quarter(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
            quarter=get_quarter_from_date(datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
            campaign_name=record.value('CampaignName'),
            campaign_id=record.value('CampaignId'),
            network=record.value('Network'),
            impressions=record.value('Impressions'),
            clicks=record.value('Clicks'),
            spend=float(record.value('Spend')) / settings['exchange_rate'],
            conversions=record.value('Conversions'),
            cost_per_conversion=float('0' + record.value('CostPerConversion')),
            value_per_conversion=float('0' + record.value('RevenuePerConversion')),
            conversion_value=float('0' + record.value('AllRevenue')),
            conversion_rate=float('0' + record.value('ConversionRate').strip('%')) / 100,
            conversion_value_per_cost=float('0' + record.value('AllReturnOnAdSpend')),
            impression_share=float('0' + record.value('ImpressionSharePercent').strip('%')),
            budget_lost_is=float('0' + record.value('ImpressionLostToBudgetPercent').strip('%')),
            rank_lost_is=float('0' + record.value('ImpressionLostToRankAggPercent').strip('%'))

        )

        campaigns_report_records_to_insert.append(report_record)

    session = get_session()
    session.bulk_save_objects(campaigns_report_records_to_insert)
    session.commit()
    # Close the session
    session.close()

    console.print(
        "Total time for adding Microsoft campaigns to the database was " + str(time.time() - tmc)[:-15] + " secs ")


def write_microsoft_search_ads_report(report_results):
    tmsa = time.time()
    ads_report_records_to_insert = []

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    microsoft_platform_fks = get_foreign_keys("microsoft_platforms")

    for record in report_results:

        # Check and make sure an empty string wasn't received. Bing... I want to strangle you!
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        # Check for shopping campaigns
        shopping_substring = "shopping"
        if shopping_substring not in record.value('CampaignName').lower():
            report_record = AdReportRecord(account=account_fks.get(clean_country_name(record.value('AccountName'))),
                                           platform=microsoft_platform_fks.get(
                                               account_fks.get(clean_country_name(record.value('AccountName')))),
                                           date=record.value('TimePeriod'),
                                           week=get_week_in_quarter(
                                               datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
                                           quarter=get_quarter_from_date(
                                               datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
                                           campaign=record.value('CampaignName'),
                                           currency='USD',
                                           impressions=record.value('Impressions'),
                                           clicks=record.value('Clicks'),
                                           spend=float(record.value('Spend')) / settings['exchange_rate'],
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

    # Get foreign keys
    account_fks = get_foreign_keys("accounts")
    microsoft_platform_fks = get_foreign_keys("microsoft_platforms")

    for record in report_results:
        if record.value('Ctr'):
            report_formatted_ctr = float(record.value('Ctr').strip('%'))
        else:
            report_formatted_ctr = 0.0

        report_record = AdReportRecord(account=account_fks.get(clean_country_name(record.value('AccountName'))),
                                       platform=microsoft_platform_fks.get(
                                           account_fks.get(clean_country_name(record.value('AccountName')))),
                                       date=record.value('TimePeriod'),
                                       week=get_week_in_quarter(
                                           datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
                                       quarter=get_quarter_from_date(
                                           datetime.strptime(record.value('TimePeriod'), '%Y-%m-%d')),
                                       campaign=record.value('CampaignName'),
                                       currency=record.value('CurrencyCode'),
                                       impressions=record.value('Impressions'),
                                       clicks=record.value('Clicks'),
                                       spend=float(record.value('Spend')) / settings['exchange_rate'],
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
