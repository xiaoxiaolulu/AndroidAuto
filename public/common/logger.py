#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  logger
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# ========================================================
import os
import sys
from termcolor import cprint
from config import parameters
from public.utils import time_util
from public.utils.variables import Variables


NOW = time_util.timestamp('format_now')

COLOR_INFO = {
    'default':
        {
            'DEBUG': 'yellow',
            'INFO': 'green',
            'ERROR': 'red',
            'WARN': 'magenta',
            'FAIL': 'grey',
            'SUCCESS': 'cyan'
        }
}

FORMAT_INFO = {
    'default':
        {
            'INFO': NOW + ' [INFO] ',
            'DEBUG': NOW + ' [DEBUG] ',
            'ERROR': NOW + ' [ERROR] ',
            'WARN': NOW + ' [WARN] ',
            'FAIL': NOW + ' [FAIL] ',
            'SUCCESS': NOW + ' [SUCCESS] '
        }
}


class MetaSingleton(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]


class ColourInfo(metaclass=MetaSingleton):

    def __init__(self, filename, mode='a', steam=None, encoding='utf-8', delay=False, count=2):
        self.filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        if steam is None:
            self.steam = sys.stderr
        self.steam = steam
        self.__console__ = sys.stdout
        self.count = count

    def __enter__(self):
        self.openedFile = open(self.filename, self.mode, encoding=self.encoding)
        return self

    @staticmethod
    def colour(msg, colour):
        return cprint(msg, colour)

    def show_message(self, level_key=None, msg=None):
        return self.colour(msg, COLOR_INFO['default'][level_key])

    def redirected_output(self, level, msg):
        for sign in range(1, self.count):
            # Record the current output pointing to the console by default
            temp = self.__console__
            if self.delay:
                self.steam = None
            else:
                with open(self.filename, self.mode, encoding=self.encoding) as file:
                    # Output to TXT file.
                    sys.stdout = file
                    self.show_message(level, msg)
                # The output is redirected back to the console.
                sys.stdout = temp
                self.show_message(level, msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.openedFile.close()


class Logger(object):

    def __init__(self):
        self.log_name = parameters.document_name('log')

    @property
    def __console__(self):
        return ColourInfo(self.log_name)

    def get_logger(self, msg, level_key=None):
        if Variables.DEBUG:
            level_key = 'DEBUG'
        return self.__console__.redirected_output(level_key, FORMAT_INFO['default'][level_key] + "".join(msg))


if __name__ == '__main__':
    L = Logger()
    L.get_logger(msg="hello world", level_key='INFO')
