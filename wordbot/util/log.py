#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
from logging.handlers import RotatingFileHandler
import os

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

FORMAT = "%(asctime)s - %(levelname)s %(filename)s:%(lineno)d %(message)s"
COLOR_FORMAT = formatter_message(FORMAT, True)
color_formatter = ColoredFormatter(COLOR_FORMAT)
log_file = '%s/../log/salebot.log' % os.path.split(os.path.realpath(__file__))[0]

fh = RotatingFileHandler(log_file, maxBytes=50*1024*1024, backupCount=5)
fh.setFormatter(color_formatter)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(color_formatter)
ch.setLevel(logging.INFO)


def get_logger(logger_name):
    loger = logging.getLogger(logger_name)
    loger.addHandler(fh)
    loger.addHandler(ch)
    loger.setLevel(logging.DEBUG)
    return loger


def log_traceback():
    with open(log_file, 'a') as f:
        traceback.print_exc()
        traceback.print_exc(file=f)
        f.flush()

if __name__ == "__main__":
    logger = get_logger('test')
    logger.debug('bar')
    logger.info('bar')
    logger.warning('bar')
    logger.error('bar')
    logger.critical('bar')
