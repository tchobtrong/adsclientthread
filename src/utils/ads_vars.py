# Copyright 2021 Mehnert GmbH or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
# Author: Chobtrong, Thitipun Email: t.chobtrong@mehnert.de

from typing import List
import logging
import re
import yaml


class Ads_Vars(object):
    '''
    List of ads variables class
    '''
    READONLY = 'R'
    WRITEREAD = 'W'
    NOTACTIVE = 'X'

    def __init__(self, filepath):
        try:
            # self.getListName(filepath)
            self.getListNameYaml(filepath)

        except Exception as e:
            errormsg = "ERROR!!!: "
            errormsg = errormsg + "Cannot read variable list: "
            errormsg = errormsg + str(e)
            logging.error(errormsg)

    def getLineInfo(self, line):
        '''
        Extract data get info
        '''
        try:
            info = re.split(':', line)
            raw_name = info[0]
            name = str(raw_name.split()[0])

            varname = name.replace('.', '_dot_')

            raw_type = info[1]
            datatype = str(raw_type.split()[0])

            return {'varname': varname,
                    'adsname': name,
                    'datatype': datatype}

        except Exception as e:
            errormsg = "ERROR!!!: "
            errormsg = errormsg + "Cannot extract varible in the list: "
            errormsg = errormsg + str(e)
            logging.error(errormsg)

            return

    def getListName(self, filepath):

        with open(filepath) as file:
            lines = file.readlines()

        for line in lines:
            info = self.getLineInfo(line)
            varname = info['varname']
            adsname = info['adsname']
            datatype = info['datatype']
            adsvar = Ads_Var(adsname, datatype)
            setattr(self, varname, adsvar)


    def getListNameYaml(self, filepath):
        '''
        Get ads symbols from yaml
        '''
        
        with open(filepath, 'r') as file:
            self.config = yaml.safe_load(file)

        if self.config is not None:

            self.writelist = list()
            self.readlist = list()

            symbollist = self.config['symbols']
            for symbol in symbollist:
                varname = str(symbol).replace('.', '_dot_')
                adsname = str(symbol)
                datatype = self.config['symbols'][adsname]['type']
                mode = self.config['symbols'][adsname]['mode']
                adsvar = Ads_Var(adsname, datatype)
                setattr(self, varname, adsvar)

                if mode == self.READONLY:
                    self.readlist.append(adsname)

                if mode == self.WRITEREAD:
                    self.readlist.append(adsname)
                    self.writelist.append(adsname)

                if mode == self.NOTACTIVE:
                    logging.info("!!! The symbol [" + str(adsname) + "] is ignored.")


class Ads_Var():
    '''
    Ads variables

    Attrs:
        adsname [STRING]: name of variable in the ads server
        datatype [STRING]: data type of the ads variable
        value [var]: Value of the variable
    '''

    def __init__(self, adsname, datatype):
        self.adsname = adsname
        self.datatype = datatype
        self.value = self.defaultvalue()

        # Create info message
        msg = "[" + self.adsname + "] "
        msg = msg + "is successfully created for ADS server."
        logging.info(msg)

    def defaultvalue(self):
        '''
        Set default data, depended on its data type
        CURRENTLY SUPPORT: BOOL, INT, BYTE

        Return:
            Default value based on the data type
        '''
        if self.datatype == 'BOOL':
            value = False
        elif self.datatype == 'INT':
            value = 0
        elif self.datatype == 'BYTE':
            value = 0
        else:
            if hasattr(self, 'adsname'):
                # create warning message
                msg = "[" + self.adsname
                msg = msg + "] has unknown datatype. Set default data to [0]"
                logging.warning(msg)
                value = 0
            else:
                # create warning message
                logging.warning("Unknown datatype. Set default data to [0]")
                value = 0
                
        return value


if __name__ == '__main__':

    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
    # adslist = Ads_Vars('adsvars.txt')
    adslist = Ads_Vars('../configs/adssymbols.yml')
    #print(str(dir(adslist)))
    value = getattr(adslist, 'Robot_INT_inputs_dot_b_UpdateParam')
    value.value = True
    print(value.adsname)  # available attributes-->>'adsname', 'datatype', 'defaultvalue', 'value'
    #print(adslist.Robot_INT_inputs_dot_b_UpdateParam.value)
    
