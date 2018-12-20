#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  start_server
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# ========================================================
from config import parameters
import yaml


def get_devices_info():
    """
    Get the test devices parameters info

    :Usage:
        get_devices_info
    """

    desired_caps = []

    with open(parameters.make_directory('data/appium_parameters.yaml', 0)) as appium_file:
        appium_parameters = yaml.load(appium_file)[0]

    with open(parameters.make_directory('data/device.yaml', 0)) as devices_file:
        for device in yaml.load(devices_file):
            desired_caps.append(dict(appium_parameters, **device))

    return desired_caps
