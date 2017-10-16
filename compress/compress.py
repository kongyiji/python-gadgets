#!/usr/bin/env python
# -*- coding: utf-8 -*-
# platform: python3

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

    # get path option in specify section
    def get_path(self, section):
        return self.config.get(section, 'Path')

if __name__ == '__main__':
    # get paths which need to compress
    ini = compress_info('config.ini')
    ini.read_config()
    sections = ini.get_section()
    paths = []
    for section in sections:
        paths.append(ini.get_path(section))
    print(sections, paths)