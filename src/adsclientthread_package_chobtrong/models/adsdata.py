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

import logging
from os import execv
import threading
import sys
from typing import List
import pyads
from utils.ads_vars import Ads_Vars


class Adsdata (object):
    '''
    A Model class contains

    The current data of ADS server
    '''

    def __init__(self, filepath):
        try:
            self.lock = threading.Lock()
            self.adsdata = Ads_Vars(filepath)
            self.readlist = list()
            self.writedict = {}
            readlist = list()

            self.setreadlist(self.adsdata.readlist)
            self.setwritelist(self.adsdata.writelist)


            # self.setreadlist(readlist)
            ## self.setwritelist(readlist)
       
        except Exception as e:
            logging.error("Cannot create ADS model: " + str(e))

    def setreadlist(self, readlist):
        for adsdata in readlist:
            adstext = adsdata.replace('.', '_dot_')
            if hasattr(self.adsdata, adstext):
                self.readlist.append(adsdata)
                msg = "Successfully add ["
                msg = msg + str(adsdata)
                msg = msg + "] in the ads readlist"
                logging.info(msg)
            else:
                errmsg = "ERROR!!: Unknow variables. Cannot add ["
                errmsg = errmsg + str(adsdata)
                errmsg = errmsg + "] in the ads readlist"
                logging.error(errmsg)

    def setwritelist(self, writelist):
        for adsdataname in writelist:
            adstext = adsdataname.replace('.', '_dot_')
            if hasattr(self.adsdata, adstext):
                adsobj = getattr(self.adsdata, adstext)              
                self.writedict[adsdataname] = adsobj.value

                # create message
                msg = "Successfully add ["
                msg = msg + str(adsdataname)
                msg = msg + "] in the ads writedict"
                logging.info(msg)
            else:
                errmsg = "ERROR!!: Unknow variables. Cannot add ["
                errmsg = errmsg + str(adsdataname)
                errmsg = errmsg + "] in the ads writedict"
                logging.error(errmsg)

    def read(self, adsdataname):
        '''
        Read single data from model

        Args:
            adsdataname [String]: Ads variable name, such as GVL.input01
        '''
        # get token
        self.lock.acquire()

        try:
            adstextname = adsdataname.replace('.', '_dot_')
            obj = getattr(self.adsdata, adstextname)

            # Release token
            self.lock.release()
            # logging.warning("Read : [" + str(adsdataname) + "] :" + str(obj.value))

            return obj.value

        except Exception as e:
            logging.warning("Cannot read : [" + str(adsdataname) + "] :" + str(e))

            # Release token
            self.lock.release()
            return

    def write(self, adsdataname, value):
        '''
        Write single data to model

        Args:
            adsdataname [String]: Ads variable name, such as GVL.input01
        '''
        # TODO: Check input data type
        # get token
        self.lock.acquire()

        try:
            adstextname = adsdataname.replace('.', '_dot_')
            obj = getattr(self.adsdata, adstextname)
            obj.value = value

            # Release token
            self.lock.release()
            return

        except Exception as e:
            logging.warning("Cannot write : [" + str(adsdataname) + "] :" + str(e))

            # Release token
            self.lock.release()
            return

    def updatereaddata(self, result):
        '''
        Update all result to the current model
        '''
        # Take token
        self.lock.acquire()

        for adsname in self.readlist:
            try:
                adstextname = adsname.replace('.', '_dot_')
                obj = getattr(self.adsdata, adstextname)
                obj.value = result[adsname]
            except Exception as e:
                logging.error("Cannot update model data [" + str(adsname) +"] :" + str(e))

        # Release token
        self.lock.release()

    def updatewritedata(self):
        '''
        Update all current model to the writedict
        '''

        # Take token
        self.lock.acquire()

        for key in self.writedict:
            try:
                adstextname = key.replace('.', '_dot_')
                obj = getattr(self.adsdata, adstextname)
                self.writedict[key] = obj.value
            
            except Exception as e:
                logging.error("Cannot update write dict [" + str(key) + "]: " + str(e))

        # Release token
        self.lock.release()

    def readads(self, plc):
        '''
        Read all data from the readlist
        '''
        
        try:
            logging.debug("Reading ADS data ...")
            result = plc.read_list_by_name(self.readlist)
            self.updatereaddata(result)
            logging.debug("Successfully read ADS data.")
            #logging.info(self.readlist)
        except Exception as e:
            logging.error("Cannot read ads data: " + str(e) + ":>> " + str(self.readlist))

    def writeads(self, plc):
        '''
        Write all data from the readlist
        '''
        self.updatewritedata()
        try:
            plc.write_list_by_name(self.writedict)
            logging.debug("Successfully write ADS data." )
            #logging.info(self.writedict)

        except Exception as e:
            logging.error("Cannot write ads data: " + str(e) + ":>> " + str(self.writedict))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
     
    adsdata_model = Adsdata('adsvars.txt')

    adsreadlist = list()
    adsreadlist.append('Robot_INT_inputs.b_Grundstellung')
    adsreadlist.append('Robot_INT_inputs.b_UpdateParam')
    adsreadlist.append('Robot_INT_inputs.b_Start')
    adsreadlist.append('Robot_INT_outputs.b_Done')
    adsreadlist.append('Robot_INT_outputs.b_ParamGelesen')
    adsreadlist.append('Robot_INT_inputs.b_test')

    adswritelist = list()
    adswritelist.append('Robot_INT_inputs.b_Grundstellung')
    adswritelist.append('Robot_INT_inputs.b_UpdateParam')
    adswritelist.append('Robot_INT_inputs.b_Start')
    adswritelist.append('Robot_INT_inputs.b_test')

    adsdata_model.setreadlist(adsreadlist)
    adsdata_model.setwritelist(adswritelist)


    try:
        plc = pyads.Connection('172.18.212.237.1.1', pyads.PORT_TC3PLC1)
        logging.debug("Successfully create plc. 172.18.212.237.1.1")
    except Exception as e: 
        logging.error("Cannot create")
    
    try:
        plc.open()
        logging.debug("Successfully open plc.")
    except Exception as e:
        logging.error("Cannot connect")
    print ("===============================")
    print(adsdata_model.readlist)
    print(adsdata_model.writedict)
    print ("===============================")
    adsdata_model.readads(plc)
    adsdata_model.writeads(plc)
    value = getattr(adsdata_model.adsdata, 'Robot_INT_inputs_dot_b_test')
    print(value.value)

    adsdata_model.write('Robot_INT_inputs_dot_b_test' , False)
    adsdata_model.updatewritedata()
    adsdata_model.writeads(plc)
    print ("===============================")
    print (adsdata_model.read('Robot_INT_inputs_dot_b_test'))