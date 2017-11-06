#!/usr/bin/env python
# -*- coding: utf-8 -*-
# platform: python3

# __author__ = Kong Yiji

import os
from datetime import date
from zipfile import ZipFile
from configparser import ConfigParser


class compress_info(object):
    '''get information'''

    # Initialization
    def __init__(self, file):
        self.file = file
        self.config = ConfigParser()

    # read configiure into mem
    def read_config(self):
        self.config.read(self.file, encoding='utf-8')

    # get all sections, except 'DEFAULT'
    def get_section(self):
        return self.config.sections()

    # get source path option in specify section
    def get_srcpath(self, section):
        return self.config.get(section, 'SourcePath')

    # get backup path option in specify section
    def get_despath(self, section):
        str_today = date.today().strftime('%Y%m%d')
        return self.config.get(section, 'BackupPath') + os.sep + str_today


def compress(srcpath, zipfilename):
    'compress source files to zipfilename'

    # open file
    with ZipFile(zipfilename, 'w') as zf:
        # traseval all path in source path
        for root, dirnames, filenames in os.walk(srcpath):
            # define relative directory
            relroot = os.path.relpath(root, start=os.path.dirname(srcpath))
            # compress all files in relative directory
            for filename in filenames:
                zf.write(os.path.join(root, filename), arcname=os.path.join(relroot, filename))


if __name__ == '__main__':
    # get paths which need to compress
    ini = compress_info('config.ini')
    ini.read_config()
    sections = ini.get_section()

    # compress every section
    for section in sections:
        # get path infomation from ini file
        srcpath = ini.get_srcpath(section)
        despath = ini.get_despath(section)
        zipfilename = despath + os.sep + section + '.zip'

        # check Source file exists or not
        if not os.path.exists(srcpath):
            print(section + ' Not Exists')

        # check Backup directory exists or not
        # Backup exists, compress
        if os.path.exists(despath):
            compress(srcpath, zipfilename)
        else:
            # Backup not exists, create directory and compress
            os.makedirs(despath)
            compress(srcpath, zipfilename)
