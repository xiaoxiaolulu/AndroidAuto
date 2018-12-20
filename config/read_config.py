#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  read_config
# Author         :  Null
# Create Date    :  2018/3/25
# Amended by     :  Null
# Amend History  :  2018/6/5
# ========================================================
import configparser
import codecs
import os


class MetaSingleton(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]


class ReadConfig(metaclass=MetaSingleton):

    def __init__(self, filename, mode='a', encoding='utf-8-sig', flag=False, sections=None, options=None, value=None):
        self.filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.sections = sections
        self.options = options
        self.value = value
        self.flag = flag
        self.__config__ = configparser.ConfigParser()

        if self.flag:
            self.__config__.add_section(self.sections)
            self.__config__.set(self.sections, self.options, self.value)
            with codecs.open(self.filename, self.mode, encoding=self.encoding) as file:
                self.__config__.write(file)

    # Read the.ini file.
    def get_data(self, section: str, option: str) -> str:
        self.__config__.read(self.filename)
        return self.__config__.get(section, option)

    # Gets the value of all of the items in the.ini file.
    def get_all(self, section: str) -> list:
        option_value = []
        self.__config__.read(self.filename)
        for option in self.__config__.options(section):
            option_value.append(self.get_data(section, option))
        return option_value


if __name__ == '__main__':
    pass
