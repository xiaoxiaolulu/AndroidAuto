#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  timeUtil
# Author         :  Null
# Create Date    :  20180731
# Amended by     :  Null
# Amend History  :  20180731
# ========================================================
import time


# 格式化时间,支持 now & day  Usage: timestamp('format_day')
def timestamp(format_key: str) -> str:
    format_time = {
        'default':
            {
                'format_day': '%Y-%m-%d',
                'format_now': '%Y-%m-%d-%H_%M_%S',
                'unix_now': '%Y-%m-%d %H:%M:%S',
            }
    }
    return time.strftime(format_time['default'][format_key], time.localtime(time.time()))


# 时间戳
def time_unix(): return int(time.mktime(time.strptime(timestamp('unix_now'), "%Y-%m-%d %H:%M:%S")))
