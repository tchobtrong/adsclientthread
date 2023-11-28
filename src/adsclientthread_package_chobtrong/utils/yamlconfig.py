# Copyright 2023 simplixio GmbH or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
# Author: Chobtrong, Thitipun Email: teddy.chobrong@gmail.com

import yaml
import logging

class yamlconfig(object):
    '''
    Yaml format configuration

    '''
    def __init__(self, configpath):

        try:
            with open(configpath, 'r') as file:
                self.config = yaml.safe_load(file)
                self.parseallconfig()
                self.validconfig = True

        except Exception as e:
            self.validconfig = False
            logging.error("Cannot read config :" + str(e))

            
    def parseallconfig(self):
        '''
        Parse all configuration
        '''
        # ADS
        self.adsserver_netid = self.config['ADS']['ads_server_netid']
        self.adstarget_username = self.config['ADS']['ads_target_username']
        self.adstarget_pw = self.config['ADS']['ads_target_pw']
        self.adsvarlistpath = self.config['ADS']['ads_var_list_path']


