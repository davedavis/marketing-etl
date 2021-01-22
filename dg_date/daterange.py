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
current_quarter = fiscalyear.FiscalQuarter.current()
last_quarter = fiscalyear.FiscalQuarter.prev_quarter

# Last Quarter Settings
# ToDo: Delete comments
company_fiscal_year = fiscalyear.FiscalYear(2020)
last_quarter_start_date = fiscalyear.FiscalQuarter.current().prev_quarter.start.strftime('%Y-%m-%d')
last_quarter_end_date = fiscalyear.FiscalQuarter.current().prev_quarter.end.strftime('%Y-%m-%d')

# last_quarter_start_date = company_fiscal_year.q3.start.strftime('%Y-%m-%d')
# last_quarter_end_date = company_fiscal_year.q3.end.strftime('%Y-%m-%d')

# bing_last_quarter_start = company_fiscal_year.q3.start
# bing_last_quarter_end = company_fiscal_year.q3.end

bing_last_quarter_start = fiscalyear.FiscalQuarter.current().prev_quarter.start
bing_last_quarter_end = fiscalyear.FiscalQuarter.current().prev_quarter.end

google_last_quarter_date_range = f'"{last_quarter_start_date}" AND "{last_quarter_end_date}"'

# Current quarter settings.
quarter_start_date = current_quarter.start.strftime('%Y-%m-%d')
quarter_current_date = fiscalyear.FiscalDateTime.now().strftime('%Y-%m-%d')
google_qtd_date_range = f'"{quarter_start_date}" AND "{quarter_current_date}"'
bing_current_quarter_start = current_quarter.start
bing_current_quarter_end = fiscalyear.FiscalDateTime.now()


# Simply return the date range objects as requested from main.
def google_thisq():
    """ Gets current quarter start date and returns a Google formatted start date date object """
    return google_qtd_date_range


def google_lastq():
    """ Gets last quarter start date and returns a Google formatted start date date object """
    return google_last_quarter_date_range


def bing_lastq_start():
    """ Gets last quarter start date and returns a Microsoft formatted start date date object """
    return bing_last_quarter_start


def bing_lastq_end():
    """ Gets last quarter start date and returns a Microsoft formatted end date date object """
    return bing_last_quarter_end


def bing_thisq_start():
    """ Gets current quarter start date and returns a Microsoft formatted start date date object """
    return bing_current_quarter_start


def bing_thisq_end():
    """ Gets current quarter start date and returns a Microsoft formatted end date date object """
    return bing_current_quarter_end


def get_google_date_range(quarter):
    google_start_date = ""
    google_end_date = ""

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


def get_adobe_date_range(quarter):
    adobe_start_date = ""
    adobe_end_date = ""

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
    if fiscalyear.FiscalQuarter.current().quarter == quarter:
        adobe_end_date = datetime.datetime.now()

        # ToDo: For debugging. Remove when stable.
        # adobe_end_date = adobe_start_date + datetime.timedelta(3)

    adobe_formatted_date_range = adobe_start_date, adobe_end_date
    return adobe_formatted_date_range


def get_bing_date_range(quarter):
    bing_start_date = ""
    bing_end_date = ""

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
    if fiscalyear.FiscalQuarter.current().quarter == quarter:
        bing_end_date = datetime.datetime.now()

    return bing_start_date, bing_end_date
