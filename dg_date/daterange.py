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

import fiscalyear

# Set up the date range object settings
fiscalyear.setup_fiscal_calendar(start_month=4)
current_quarter = fiscalyear.FiscalQuarter.current()
last_quarter = fiscalyear.FiscalQuarter.prev_quarter

# Last Quarter Settings
# ToDo: Calculate hard coded Q2 in last quarter
company_fiscal_year = fiscalyear.FiscalYear(2021)
last_quarter_start_date = company_fiscal_year.q2.start.strftime('%Y-%m-%d')
last_quarter_end_date = company_fiscal_year.q2.end.strftime('%Y-%m-%d')
bing_last_quarter_start = company_fiscal_year.q2.start
bing_last_quarter_end = company_fiscal_year.q2.end
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





