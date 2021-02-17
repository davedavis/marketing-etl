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

# ToDo: Add the correct data in here.

def get_skews(quarter):
    # ToDo, actually get the skews.

    records_to_insert = [
        ("UK", 492693, 2458665, 0.20, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
        ("IE", 51965, 409777, 0.13, 0.02, 0.1, 0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 0.07, 0.07, 0.1, 0.08, 0.08, 0.03),
        ("DE", 729221, 3698601, 0.20, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("AT", 111815, 821338, 0.14, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("CH", 157896, 1044068, 0.15, 0.03, 0.07, 0.07, 0.07, 0.08, 0.08, 0.07, 0.08, 0.08, 0.12, 0.08, 0.08, 0.08, 0.04),
        ("FR", 230684, 1120651, 0.20, 0.02, 0.06, 0.07, 0.09, 0.09, 0.09, 0.11, 0.07, 0.11, 0.06, 0.06, 0.06, 0.07, 0.03),
        ("ES", 95035, 545993, 0.17, 0.06, 0.06, 0.06, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.09, 0.08, 0.08, 0.08, 0.04),
        ("IT", 127896, 816425, 0.16, 0.03, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("PT", 16885, 60524, 0.27, 0.05, 0.06, 0.06, 0.07, 0.08, 0.08, 0.09, 0.07, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
        ("NO", 26584, 150431, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("SE", 44339, 243477, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("FI", 23039, 133146, 0.17, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("DK", 83330, 553985, 0.15, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.13, 0.08, 0.1, 0.08, 0.08, 0.08, 0.08, 0.04),
        ("NL", 110166, 604416, 0.18, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03),
        ("BE", 73444, 450679, 0.16, 0.02, 0.05, 0.07, 0.08, 0.07, 0.08, 0.12, 0.08, 0.09, 0.08, 0.08, 0.08, 0.08, 0.03)
    ]

    write_skews(records_to_insert)