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

import threading
import time
import datetime
from threading import Thread, Event
import logging
import pyads
from models.adsdata import Adsdata
from utils.yamlconfig import yamlconfig


class AdsClienthandler(Thread):
    '''
    An handler class

    ADS client for controlling cameras
    '''

    def __init__(self, handlername, 
                run_event:Event, 
                config:yamlconfig,
                adsmodel:Adsdata)-> None:

        # init process attrributes
        Thread.__init__(self, target=None, name=handlername)
        self.lock = threading.Lock()
        self.adsmodel = adsmodel
        self.run_event = run_event
        self.config = config
        self.isconnected = False
        self.isReadyToStop = False

        # Checking PLC connection
        self.testconnection()


    def testconnection(self):
        '''
        Test connection to ADS server
        '''
        try:
            logging.info("Testing connection to ADS server ...")
            self.plc = pyads.Connection(self.config.adsserver_netid,
                                        pyads.PORT_TC3PLC1)
            self.plc.open()
            self.isconnected = True
            logging.info("Successfully connected to ADS Server.")
            self.plc.close()

        except Exception as e:
            errmsg = "ERROR!: cannot connect to ADS server :"
            errmsg = errmsg + str(e)
            logging.error(errmsg)


    def run(self):
        '''
        Overwrite run method of Thread
        '''
        if self.isconnected:

            try:
                # Build connection
                self.plc = pyads.Connection(self.config.adsserver_netid,
                                        pyads.PORT_TC3PLC1)
                self.plc.open()

                # check if all sysbols exists in the target plc
                notFoundSymbol = self.adsmodel.checkallsymbols(self.plc)

                if notFoundSymbol:
                    logging.error("Cannot find all ads symbols. Terminate the ads client thread")


            except Exception as e:
                logging.error("Cannot connect to ADS server: " + str(e))

            while self.run_event.is_set() and not notFoundSymbol:

                try:

                    # Write ads data
                    self.adsmodel.writeads(self.plc)
                    # Read ads data
                    self.adsmodel.readads(self.plc)

                    time.sleep(0.01)

                except Exception as e:
                    logging.error("ERROR!: cannot read/write ADS server :" +str(e))
                    break

        else:
            logging.error("Cannot connect to ADS Server. Thread stop.")


    def stop(self):
        '''
        Stop all threads
        '''

        logging.info("Terminating all service threads ... ")

        # terminate main thread
        logging.info("Terminating main thread ... ")
        self.isReadyToStop = True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(threadName)s %(message)s')

    logging.info("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    logging.info("(((((((((((((((/*((((((((((((((((((((((((((((((((((");
    logging.info("((((((((((((        (((((((((((((((((((((((((((((((");
    logging.info("((((((((((((         ((((((((((((((((((((((((((((((");
    logging.info("(((((((((((((      ((((((((((((((((((((((((((((((((");
    logging.info("((((((((((((((((((((((((((((*. .(((((((((((((((((((");
    logging.info("((((((((((((((     (((((            /((((((((((((((");
    logging.info("((((((((((((((     ((((     ((((     ((((((((((((((");
    logging.info("((((((((((((((     ((((     (((((     (((((((((((((");
    logging.info("((((((((((((((     (((/     (((((     (((((((((((((");
    logging.info("((((((((((((((     (((/     (((((     (((((((((((((");
    logging.info("((((((((((((((     ((((     (((((     (((((((((((((");
    logging.info("((((((((((((((     ((((     ((((,    *(((((((((((((");
    logging.info("((((((((((((((     (((((             ((((((((((((((");
    logging.info("((((((((((((((,,,,,(((((((/       (((((((((((((((((");
    logging.info("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    logging.info("((((((((((((/                         (((((((((((((");
    logging.info("((((((((((((/                         (((((((((((((");
    logging.info("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    logging.info("***************************************************");
    logging.info("*** ads client thread powered by simplixio    *****");
    logging.info("***************************************************");

    logging.info("Initializing ....")

    # Init run event
    run_event = threading.Event()

    #Get config
    config = yamlconfig(configpath='./configs/config.yml')

    # Init ads data models with ads symbol list
    adsmodel = Adsdata(filepath='./configs/adssymbols.yml')

    # Set run event
    run_event.set()

    # Init the ads client thread
    adsclienthandler = AdsClienthandler(handlername="ADS client",
                                        run_event=run_event,
                                        config=config,
                                        adsmodel=adsmodel)
    
    # Start thread
    adsclienthandler.start()
    
     # Stop when KeyboardInterrupt
    try:
        while 1:
            if adsclienthandler.isReadyToStop:
                adsclienthandler.join()
                break
            time.sleep(0.1)

    except KeyboardInterrupt:
        logging.info("Terminating ... ")
        run_event.clear()
        adsclienthandler.stop()
        if adsclienthandler.isReadyToStop:
            adsclienthandler.join()

    logging.info("Threads successfully closed")
    exit

