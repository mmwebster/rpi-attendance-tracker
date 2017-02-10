#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import time
from os import environ as ENV
import csv

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Utility functions
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class LocalStorage():
    def __init__(self, drive_path):
        self.drive_path = drive_path
        # load values contained in config file
        self.config = {}
        self.load_config_file()
        # hash of when the student checked in, if they have
        self.time_in_entries = {}

    # @desc Opens config file, stores all of its key/value pairs, then closes it
    def load_config_file(self):
        with open(self.drive_path + "config.csv", 'r') as config_file:
            config_file_reader = csv.reader(config_file)

            for row in enumerate(config_file_reader):
                self.config[str(row[1][0]).strip()] = str(row[1][1]).strip()
                print("storing (" + str(row[1][0]).strip() + "," + str(row[1][1]).strip() + ")")

    def read_config_value(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return "NOT_FOUND"

    def append_rows(self, file_name, data):
        with open(self.drive_path + "/" + file_name, 'ab') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
