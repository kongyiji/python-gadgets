#!/usr/bin/env python
# -*- coding: utf-8 -*-
# platform: python3

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
        self.config.read(self.file)

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
    with ZipFile(zipfilename, 'w') as zf:
        for root, dirnames, filenames in os.walk(srcpath):
            relroot = os.path.relpath(root, start=os.path.dirname(srcpath))
            # print(relroot)
            for filename in filenames:
                # print(os.path.join(root, filename))
                zf.write(os.path.join(root, filename), arcname=os.path.join(relroot, filename))

if __name__ == '__main__':
    # get paths which need to compress
    ini = compress_info('config.ini')
    ini.read_config()
    sections = ini.get_section()
    for section in sections:
        srcpath = ini.get_srcpath(section)
        despath = ini.get_despath(section)
        zipfilename = despath + os.sep + section + '.zip'
        os.chdir(srcpath)
        # print(srcpath, despath, zipfilename)
        compress(srcpath, zipfilename)
    # print(sections, srcpaths, despaths)