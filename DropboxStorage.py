#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import time
import dropbox
from os import environ as ENV

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Utility functions
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class DropboxStorage():
    def __init__(self, auth_token, drive_path):
        self.auth_token = auth_token
        self.drive_path = drive_path
        self.dbx = dropbox.Dropbox(self.auth_token)

    # @desc Opens config file, stores all of its key/value pairs, then closes it
    def upload(self, file_name):
        with open(self.drive_path + "/" + file_name, 'rb') as f:
            self.dbx.files_upload(f.read(), "/" + file_name)

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
