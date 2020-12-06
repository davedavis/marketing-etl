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


# Load the country accounts into a dict from the YAML file.
import yaml
import os


def get_settings():
    if os.environ['DG_ENV']:
        with open('dg_config/settings.dev.yaml', 'r') as f:
            settings_file = yaml.load(f, Loader=yaml.SafeLoader)
            selected_settings = dict(settings_file)
    else:
        with open('dg_config/settings.dev.yaml', 'r') as f:
            settings_file = yaml.load(f, Loader=yaml.SafeLoader)
            selected_settings = dict(settings_file)

    return selected_settings


def get_settings_file_path():
    if os.environ['DG_ENV']:
        settings_file_path_string = 'dg_config/settings.dev.yaml'
    else:
        settings_file_path_string = 'dg_config/settings.dev.yaml'

    return settings_file_path_string
