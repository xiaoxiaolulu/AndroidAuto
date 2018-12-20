#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  parameters
# Author         :  Null
# Create Date    :  20180325
# Amended by     :  Null
# Amend History  :  20180701
# ========================================================
import os
from config.read_config import ReadConfig
from public.utils import time_util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

READ_CONF = ReadConfig(os.path.join(os.path.dirname(__file__), 'config.ini'))


# DATABASE SETTING
DATABASES = {
    'default': {
        'host': READ_CONF.get_data('MysqlTest', 'host'),
        'port': int(READ_CONF.get_data('MysqlTest', 'port')),
        'user': READ_CONF.get_data('MysqlTest', 'user'),
        'passwd': READ_CONF.get_data('MysqlTest', 'password'),
        'db': READ_CONF.get_data('MysqlTest', 'db'),
        'charset': "utf8"
    }
}


# 创建当前时间 日志 & 测试报告, Usage: make_directory('Case', 0)
def make_directory(root_directory: str, extension_pattern: int, flag: 'default False'=False) -> str:
    extension_root = os.path.abspath(os.path.join(BASE_DIR, root_directory.lower()))
    file_directory = [
        extension_root,
        extension_root + '/log/' + time_util.timestamp('format_day'),
        extension_root + '/report/' + time_util.timestamp('format_day'),
        extension_root + '/img/' + time_util.timestamp('format_day'),
        extension_root + '/log/',
        extension_root + '/report/',
        extension_root + '/img/'
    ]

    if not os.path.exists(extension_root):
        os.mkdir(extension_root)

    for filename in file_directory:
        if not os.path.exists(filename) and flag is True:
            os.makedirs(os.path.abspath(filename))

    return file_directory[extension_pattern]


# 指定创建当前时间的LOG 文件 或 HTML 报告, Usage: document_name('log')
def document_name(extension_filename: str, filename: 'default Null'='', flag: 'default False'=True) -> str:
    document_index = {'log': 1, 'html': 2, 'img': 3}
    extension_document = make_directory('result', int(document_index[extension_filename]), flag)
    filename = os.path.abspath(
        os.path.join(
            extension_document,
            '{0}{1}.{2}'.format(time_util.timestamp('format_now'), filename, extension_filename)
        )
    ) \
        if filename is None else os.path.abspath(
        os.path.join(
            extension_document,
            '{0}.{1}'.format(filename, extension_filename
                             )
        )
    )
    return filename


# EMAIL SETTING
EMAILS = {
    'default': {
        'receivers': READ_CONF.get_all('EmailReceivers'),
        'sender_name': READ_CONF.get_data('EmailSender', 'sendaddr_name'),
        'sender_psw': READ_CONF.get_data('EmailSender', 'sendaddr_pswd'),
        'filename': make_directory('Result', 2)
    }
}
