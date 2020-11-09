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

import mysql
import yaml
from mysql.connector import connection

# Init settings
from dg_config import settingsfile

settings = settingsfile.get_settings()



def connect():
    global_connection = mysql.connector.connect(host=settings['db_host'],
                                                user=settings['db_user'],
                                                password=settings['db_password'],
                                                database=settings['db_database']
                                                )
    return global_connection
