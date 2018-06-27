#!/usr/bin/env python
# -*- coding: utf-8 -*-
# platform: python3

# __author__ = Kong Yiji

import os
import chardet
import subprocess
from logger import log
from datetime import date
from zipfile import ZipFile
from configparser import ConfigParser, NoOptionError

compress_log = log('compress')

class compress_info(object):
    """get information"""

    # Initialization
    def __init__(self, file):
        self.file = file
        self.config = ConfigParser()

    # read configiure into mem
    def read_config(self):
        with open(self.file, 'rb') as f:
            cache = f.read()
            filecode = chardet.detect(cache)['encoding']
        self.config.read(self.file, encoding=filecode)
        compress_log.info('load config file')

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

    # get WinRAR path
    def get_rarpath(self, section):
        return self.config.get(section, 'RARPath')


def compress(srcpath, zipfilename):
    """compress source files to zipfile name"""

    # open file
    with ZipFile(zipfilename, 'w') as zf:
        # search all path in source path
        for root, dirnames, filenames in os.walk(srcpath):
            # define relative directory
            relroot = os.path.relpath(root, start=os.path.dirname(srcpath))
            # compress all files in relative directory
            for filename in filenames:
                zf.write(os.path.join(root, filename), arcname=os.path.join(relroot, filename))
                compress_log.info('compressing file [%s] to [%s]' % (filename, zipfilename))


def compress_rar(rarpath, rarfilename, srcpath):
    """compress source files to rarfile name"""

    # abspath = os.path.join(srcpath, relpath)
    # command not delete source files
    rar_command = '"%s" a -ep1 -r -m5 -ma5 -inul "%s" "%s"' % (rarpath, rarfilename, srcpath)

    # command delete source files
    # rar_command = '"%s" a -ep1 -r -m5 -ma5 -inul -df "%s" "%s"' % (rarpath, rarfilename, srcpath)

    subprocess.call(rar_command)
    compress_log.info('compressing directory [%s] to [%s]' % (srcpath, rarfilename))


def main():
    # Initailize
    rarpath = None

    # get paths which need to compress
    ini = compress_info('config.ini')
    ini.read_config()
    sections = ini.get_section()
    # if exists, get WinRAR path
    try:
        rarpath = ini.get_rarpath('DEFAULT') + os.sep + 'Rar.exe'
        compress_log.info('compress with RAR format')
    except NoOptionError as e:
        compress_log.info('compress with ZIP format')

    # compress every section
    for section in sections:
        # get path information from ini file
        srcpath = ini.get_srcpath(section)
        despath = ini.get_despath(section)
        zipfilename = despath + os.sep + section + '.zip'
        rarfilename = despath + os.sep + section + '.rar'

        # check Source file exists or not
        if not os.path.exists(srcpath):
            print(section + ' Not Exists, Nothing will be compress.')
            compress_log.warning('%s not exists. Nothing will be compress.' % section)
            continue

        # check use WinRAR or not to compress
        if rarpath:
            # check Backup directory exists or not
            # Backup exists, compress
            if os.path.exists(despath):
                compress_rar(rarpath, rarfilename, srcpath)
            else:
                # Backup not exists, create directory and compress
                os.makedirs(despath)
                compress_rar(rarpath, rarfilename, srcpath)
        else:
            # check Backup directory exists or not
            # Backup exists, compress
            if os.path.exists(despath):
                compress(srcpath, zipfilename)
            else:
                # Backup not exists, create directory and compress
                os.makedirs(despath)
                compress(srcpath, zipfilename)


if __name__ == '__main__':
    main()
