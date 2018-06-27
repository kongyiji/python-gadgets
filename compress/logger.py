#!/usr/bin/env python
# -*- coding: utf-8 -*-
# platform: python 3

import os
from logbook import Logger, TimedRotatingFileHandler, set_datetime_format


def log(app_name):
    """use logbook to log """

    # use local time zone
    set_datetime_format('local')
    # check log dir
    log_dir = os.path.join('.', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # set log handler type
    TimedRotatingFileHandler(os.path.join(log_dir, '%s.log' % app_name),
                             date_format='%Y%m%d', bubble=True).push_application()
    app_logger = Logger(app_name)
    return app_logger


if __name__ == '__main__':
    test_log = log('test')
    test_log.info('test log file')
