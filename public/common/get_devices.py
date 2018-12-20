#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  get_devices
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# ========================================================
import yaml
import subprocess
from public.utils import adb
from public.common import logger
from config import parameters


def get_android_devices():
    """
    Acquisition test equipment

    :Usage:
        get_devices()
    """
    android_devices_list = []
    devices = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for device in devices.stdout.readlines():
        if isinstance(device, (bytes, bytearray)):
            device = device.decode('utf-8')
        if 'device' in device and 'devices' not in device:
            android_devices_list.append(device.split('\t')[0])

    return android_devices_list


def save_devices_yaml():
    """
    The test device information is saved to yaml

    :Usage:
        save.devices_yaml()
    """

    device_list = []
    for device in get_android_devices():
        cmd = adb.Adb(device)
        device_list.append(
            {'deviceName': device, 'platformName':
                'Android', 'platformVersion': cmd.device_version()})
        logger.Logger().get_logger(
            'Get the android device is {0}, android version is {1}'.format(
                device, cmd.device_version()))

    with open(parameters.make_directory('data/device.yaml', 0), 'w') as f:
        yaml.dump(device_list, f)
