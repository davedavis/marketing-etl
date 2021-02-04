#  #!/usr/bin python

#  Copyright (c) 2021.  Dave Davis
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

import sys

from dg_config import settingsfile
from dg_db.db_write import write_skews
from rich.console import Console

console = Console()
settings = settingsfile.get_settings()

def get_skews(quarter):
    # ToDo, actually get the skews.
    records_to_insert = [
    ("UK", 296238.89, 159513.25, 12, 2.06, 9.58, 7.75, 7.75, 7.50, 7.38, 7.38, 7.38, 7.38, 7.38, 10.31, 7.51, 7.63, 3.00),
    ("IE", 32915.43, 17723.69, 12, 2.06, 9.58, 7.75, 7.75, 7.50, 7.38, 7.38, 7.38, 7.38, 7.38, 10.31, 7.51, 7.63, 3.00),
    ("DE", 461892.23, 248711.2, 12, 3.00, 6.50, 7.00, 7.00, 7.50, 7.50, 7.00, 8.00, 7.50, 11.50, 8.00, 7.50, 8.00, 4.00),
    ("AT", 70824.53, 38136.29, 12, 3.00, 6.50, 7.00, 7.00, 7.50, 7.50, 7.00, 8.00, 7.50, 11.50, 8.00, 7.50, 8.00, 4.00),
    ("CH", 100012.32, 53852.79, 12, 3.00, 6.50, 7.00, 7.00, 7.50, 7.50, 7.00, 8.00, 7.50, 11.50, 8.00, 7.50, 8.00, 4.00),
    ("FR", 146116.23, 78677.97, 12, 2.42, 5.50, 6.60, 9.00, 9.00, 9.00, 11.00, 7.00, 10.88, 6.40, 6.40, 6.40, 7.00, 3.40),
    ("ES", 60195.88, 32413.17, 12, 2.42, 5.50, 6.60, 9.00, 9.00, 9.00, 11.00, 7.00, 10.88, 6.40, 6.40, 6.40, 7.00, 3.40),
    ("IT", 81009.99, 43620.76, 12, 2.42, 5.50, 6.60, 9.00, 9.00, 9.00, 11.00, 7.00, 10.88, 6.40, 6.40, 6.40, 7.00, 3.40),
    ("PT", 10695.6, 5759.17, 12, 2.42, 5.50, 6.60, 9.00, 9.00, 9.00, 11.00, 7.00, 10.88, 6.40, 6.40, 6.40, 7.00, 3.40),
    ("NO", 16838.76, 9067.02, 12, 2.00, 4.50, 7.00, 8.00, 7.00, 7.50, 13.00, 7.50, 10.00, 7.50, 7.50, 7.50, 7.50, 3.50),
    ("SE", 28085.01, 15122.7, 12, 2.00, 4.50, 7.00, 8.00, 7.00, 7.50, 13.00, 7.50, 10.00, 7.50, 7.50, 7.50, 7.50, 3.50),
    ("FI", 14593.59, 7858.09, 12, 2.00, 4.50, 7.00, 8.00, 7.00, 7.50, 13.00, 7.50, 10.00, 7.50, 7.50, 7.50, 7.50, 3.50),
    ("DK", 52781.85, 28421, 12, 2.00, 4.50, 7.00, 8.00, 7.00, 7.50, 13.00, 7.50, 10.00, 7.50, 7.50, 7.50, 7.50, 3.50),
    ("NL", 69779.81, 37573.74, 12, 2.00, 4.50, 6.80, 8.40, 7.00, 7.50, 12.40, 7.50, 9.40, 8.40, 7.80, 7.80, 7.50, 3.00),
    ("BE", 46519.87, 25049.16, 12, 2.00, 4.50, 6.80, 8.40, 7.00, 7.50, 12.40, 7.50, 9.40, 8.40, 7.80, 7.80, 7.50, 3.00)
    ]

    write_skews(records_to_insert)
