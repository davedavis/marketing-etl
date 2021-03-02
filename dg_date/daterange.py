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
import datetime

import fiscalyear

# Set up the date range object settings
fiscalyear.setup_fiscal_calendar(start_year='same', start_month=4)


def get_google_date_range(quarter, year):
    google_start_date = ""
    google_end_date = ""

    if year == "last":
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=455)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)
    else:
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=90)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)

    if quarter == 1:
        google_start_date = company_fiscal_year.q1.start.strftime('%Y-%m-%d')
        google_end_date = company_fiscal_year.q1.end.strftime('%Y-%m-%d')
    elif quarter == 2:
        google_start_date = company_fiscal_year.q2.start.strftime('%Y-%m-%d')
        google_end_date = company_fiscal_year.q2.end.strftime('%Y-%m-%d')
    elif quarter == 3:
        google_start_date = company_fiscal_year.q3.start.strftime('%Y-%m-%d')
        google_end_date = company_fiscal_year.q3.end.strftime('%Y-%m-%d')
    elif quarter == 4:
        google_start_date = company_fiscal_year.q4.start.strftime('%Y-%m-%d')
        google_end_date = company_fiscal_year.q4.end.strftime('%Y-%m-%d')
    else:
        print("You didn't pass in a valid quarter number. Options are 1, 2, 3 or 4")

    google_formatted_date_range = f'"{google_start_date}" AND "{google_end_date}"'
    return google_formatted_date_range


def get_adobe_date_range(quarter, year):
    adobe_start_date = ""
    adobe_end_date = ""

    if year == "last":
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=455)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)
    else:
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=90)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)

    if quarter == 1:
        adobe_start_date = company_fiscal_year.q1.start
        adobe_end_date = company_fiscal_year.q1.end
    elif quarter == 2:
        adobe_start_date = company_fiscal_year.q2.start
        adobe_end_date = company_fiscal_year.q2.end
    elif quarter == 3:
        adobe_start_date = company_fiscal_year.q3.start
        adobe_end_date = company_fiscal_year.q3.end
    elif quarter == 4:
        adobe_start_date = company_fiscal_year.q4.start
        adobe_end_date = company_fiscal_year.q4.end
    else:
        print("You didn't pass in a valid quarter number. Options are 1, 2, 3 or 4")

    # If the requested quarter is this quarter, set the end date to today, and not the end of the quarter as Microsoft
    # Ads doesn't support using future dates (and ignoring them) in the API like Google does.
    if fiscalyear.FiscalQuarter.current().quarter == quarter and year != "last":
        adobe_end_date = datetime.datetime.now()

    joined_ranges = str(adobe_start_date) + ".000/" + str(adobe_end_date)[:-3]
    # Add in the Ts
    adobe_formatted_date_range = "T".join(joined_ranges.split())
    return adobe_formatted_date_range


def get_bing_date_range(quarter, year):
    bing_start_date = ""
    bing_end_date = ""

    if year == "last":
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=455)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)
    else:
        report_fiscal_year = datetime.datetime.now() - datetime.timedelta(days=90)
        company_fiscal_year = fiscalyear.FiscalYear(report_fiscal_year.year)

    if quarter == 1:
        bing_start_date = company_fiscal_year.q1.start
        bing_end_date = company_fiscal_year.q1.end
    elif quarter == 2:
        bing_start_date = company_fiscal_year.q2.start
        bing_end_date = company_fiscal_year.q2.end
    elif quarter == 3:
        bing_start_date = company_fiscal_year.q3.start
        bing_end_date = company_fiscal_year.q3.end
    elif quarter == 4:
        bing_start_date = company_fiscal_year.q4.start
        bing_end_date = company_fiscal_year.q4.end
    else:
        print("You didn't pass in a valid quarter number. Options are 1, 2, 3 or 4")

    # If the requested quarter is this quarter, set the end date to today, and not the end of the quarter as Microsoft
    # Ads doesn't support using future dates (and ignoring them) in the API like Google does.
    if fiscalyear.FiscalQuarter.current().quarter == quarter and year != "last":
        bing_end_date = datetime.datetime.now()

    return bing_start_date, bing_end_date
