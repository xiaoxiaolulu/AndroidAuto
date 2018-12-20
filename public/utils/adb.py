#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  adb
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# ========================================================
import os
import time
import random
import re
import socket
import platform
from config import parameters
from public.common import logger
from public.utils.variables import KeyCode

# To determine the system type,
# Windows USES findstr and Linux USES grep
system = platform.system()
find_command = 'findstr' if system == 'Windows' else 'grep'

# Automatically sets the environment variable for ANDROID_HOME
if 'ANDROID_HOME' in os.environ:
    if system == 'Windows':
        command = os.path.join(
            os.environ['ANDROID_HOME'],
            'platform-tools',
            'adb.exe'
        )
    else:
        command = os.path.join(
            os.environ['ANDROID_HOME'],
            'platform-tools',
            'adb'
        )


class Adb(object):

    def __init__(self, device=None):
        if device is not None:
            self.device = '-s {0}'.format(device)
        else:
            self.device = ''

    def adb_arguments(self, args):
        return os.popen('adb {0} {1}'.format(self.device, args)).readlines()

    def shell_arguments(self, args):
        return os.popen('adb {0} shell {1}'.format(self.device, args)).readlines()

    def device_name(self):
        """
        Get device name

        :Usage:
            Adb().device_name()
        """
        return self.shell_arguments('getprop ro.serialno')[0]

    def device_version(self):
        """
        Get the device version number.

        :Usage:
            device_version()
        """
        return self.shell_arguments('getprop ro.build.version.release')[0].strip()

    def resolved_package(self, keyword):
        """
        Gets the application name to be tested.

        :Args:
         -keyword: Search keyword, STR TYPE.

        :Usage:
            Adb().resolved_package('rpms')
        """
        package_list = self.shell_arguments('pm list packages')
        for index, value in enumerate(package_list):
            if str(package_list[index]).find(keyword) != -1:
                return str(value).split(':')[1]

    def install_apk(self, apk_name):
        """
        Install apk
        :Args:
         - apk_name: The app package name, STR TYPE

        :Usage:
            Adb().install_apk(apk_name)
        """
        self.adb_arguments('install {0}'.format(apk_name))

    def is_install(self, apk_name):
        """
        Check install apk status

        :Args:
         - apk_name: The app package name, STR TYPE.

        :Usage:
            Adb().is_install(apk_name)
        """
        return True if self.resolved_package(apk_name) else False

    def uninstall(self, apk_name):
        """
        Uninstall apk

        :Args:
         - apk_name: The app package name, STR TYPE.

        :Usage：
            Adb().uninstall(apk_name)
        """
        self.adb_arguments('unintsall {0}'.format(apk_name))

    def get_activity(self, package):
        """
        Gets the Activity at the start of the application.

        :Args:
         - package: The app package name, STR TYPE.

        :Usage:
            Adb().get_activity('com.tdh.rpms')
        """
        context = self.shell_arguments('dumpsys package {0}'.format(package))
        for index, value in enumerate(context):
            if 'SplashActivity' in context[index]:
                return str(value.strip()).split()[1].replace('/', '')

    def check_devices(self):
        """
        Check the connection to android devices.

        :Usage:
            Adb().check_devices()
        """
        connect_status = self.adb_arguments('devices')
        if len(connect_status) > 2:
            device_name = str(connect_status[1]).strip('\t\n')[:str(connect_status[1]).strip('\t\n').find('device')]
            if device_name is not None:
                return True

    def device_ip(self):
        """
        Get the android device IP address.

        :Usage:
            Adb().device_ip()
        """
        device_ip = self.shell_arguments('netcfg')
        for index, value in enumerate(device_ip):
            if 'wlan' in device_ip[index]:
                pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
                match = re.findall(pattern, value)
                return match[0]

    def clear_data(self, package):
        """
        Clear application data and cache.

        :Args:
         - package: The app package name, STR TYPE.

        :Usage:
            Adb().clear_data('com.thd.rpms')
        """
        return True if 'Success' in self.shell_arguments('pm clear {0}'.format(package))[0].strip() else False

    def device_status(self):
        """
        Get device status

        Device: normal connection
        offline: connection is abnormal, and the device is unresponsive
        unknown: there is no connection device

        :Usage:
            Adb().device_status()
        """
        return self.adb_arguments('get-state')[0].strip()

    def reboot(self):
        """
        Equipment to restart

        :Usage:
            Adb().reboot()
        """
        self.adb_arguments('reboot')

    @staticmethod
    def get_new_apk():
        """
        Get the latest Apk package name

        :Usage:
            Adb().get_new_apk()
        """
        try:
            apk_dir = os.listdir(parameters.document_name('apk'))
            if len(apk_dir) == 0:
                logger.Logger().get_logger('Everything in the the document!', 'ERROR')
            apk_dir.sort()
            return apk_dir[-1]
        except FileNotFoundError as error:
            logger.Logger().get_logger('The FileNotFoundError is {0}!'.format(error))

    def get_apk_version(self, apk):
        """
        Get the apk version

        :Args:
         - apk: Apk package name, STR TYPE.

        :Usage:
            Adb().get_apk_version()
        """
        version_name = self.shell_arguments('dumpsys package {0} | {1} "versionName"'.format(apk, find_command))
        apk_version = str(version_name[0]).split('=')[1].strip('\n')
        now_version = str(self.get_new_apk().split('_')[2]).replace('.apk', '')
        return True if apk_version == now_version else False

    def get_apk_size(self):
        """
        Get the size of the APK

        :Usage:
            Adb().get_apk_size()
        """
        apk_size = os.path.getsize(os.path.join(parameters.document_name('apk'), self.get_new_apk()))/(1024*1024)
        logger.Logger().get_logger('The apk size is {0}MB'.format(apk_size))
        return round(apk_size, 2)

    def get_android_id(self):
        """
        Get android_id

        :Usage:
            Adb().get_android_id()
        """
        return self.shell_arguments('settings get secure android_id')[0].strip()

    def get_device_id(self):
        """
        Get device id

        :Usage:
            Adb().get_device_id()
        """
        return self.adb_arguments('get-serialno')[0].strip()

    def get_pid(self, apk_name):
        """
        Get the device PID

        :Args:
         - apk_name: Apk package name, STR TYPE.

        :Usage:
            Adb().get_pid('com.tdh.rpms')
        """
        content = self.shell_arguments('ps | {0} {1}'.format(find_command, apk_name))
        return str(content[0]).split()[1]

    def get_uid(self, apk_name):
        """
        Get the device Uid

        :Args:
         - apk_name: APK package name, STR TYPE

        :Usage:
            Adb().get_uid('com.tdh.rpsm')
        """
        content, uid = self.shell_arguments('cat /proc/{0}/status'.format(self.get_pid(apk_name))), []
        for line in content:
            if 'Uid' in line:
                uid.append(str(line).split('\t')[1])
        return uid[0]

    def get_the_device_size(self):
        """
        Get the device screen size

        :Usage:
            Adb().get_the_device_size()
        """
        devices_size = self.shell_arguments('wm size')
        return str(devices_size[0]).split(':')[1].strip()

    def get_the_current_device_network(self):
        """
        View the current device network

        :Usage:
            Adb().get_the_current_device_network()
        """
        devices_network = self.shell_arguments('netcfg')
        for network in devices_network:
            if 'wlan0' in network:
                return str(network.split()[2]).split('/')[0]

    def input_key_code(self, key_code):
        """
        Simulate phone button/input

        :Args:
         - key_code: Physical button of mobile phone, INT TYPE.

        :Usage:
            Adb().input_key_code(3)
        """
        self.shell_arguments('input keyevent {code}'.format(code=key_code))
        time.sleep(0.1)

    def key_event(self, key):
        """
        Common physical key operation

        :Args:
         - key: the physical button of mobile phone ’s codes key, STR TYPE.

        :Usage:
            Adb().key_event()
        """
        self.input_key_code(getattr(KeyCode, key))


if __name__ == '__main__':
    A = Adb()
    # @staticmethod
    # def kill_port(occupied_port):
    #     """
    #     杀掉占用指定端口的进程
    #     :param occupied_port:   将要指定的端口号
    #     :return:                返回布尔值True
    #     """
    #     ports_used = os.popen('netstat -ano').readlines()
    #     # ports_dict key is port, value is pid
    #     ports_dict = {}
    #     for index, value in enumerate(ports_used):
    #         if index >= 4 and 'LISTENING' in value:
    #             ports_dict[value[str(value).find(':') + 1:str(value).find(':') + 5].strip()] = value[str(value).find('LISTENING') + len('LISTENING'):].strip()
    #         for key, val in ports_dict.items():
    #             # Kill the occupied process
    #             if occupied_port == key:
    #                 progress = os.popen('tasklist|findstr %s' % val).readlines()
    #                 for pro_name in progress:
    #                     progress_name = pro_name[:str(pro_name).find('exe') + len('exe')]
    #                     result = os.popen('taskkill /f /t /im %s' % progress_name).readlines()
    #                     for result_context in result:
    #                         if '成功' in str(result_context).strip('\n'):
    #                             print('Successful kill process: %s' % progress_name)
    #                             return True
    #

    #

    #
    # def is_free(self, port, ip='127.0.0.1'):
    #     """
    #     判断端口是否被占用
    #     :param port:        端口号，int类型
    #     :param ip:          ip地址，默认127.0.0.1
    #     :return:            返回布尔值，True或False
    #     """
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         sock.connect((ip, port))
    #         self.log.info('Server port %s OK' % port)
    #         return True
    #     except Exception as error:
    #         self.log.error(error)
    #         return False
    #     finally:
    #         sock.close()
    #
    # @staticmethod
    # def get_port(num):
    #     """
    #     生成一组随机的端口数组
    #     :param num:         循环次数，int类型
    #     :return:            端口数组
    #     """
    #     flag, port_list = 0, []
    #     while flag < num:
    #         port = random.randint(4700, 4900)
    #         port_list.append(port)
    #         flag += 1
    #     return port_list
    #
    # def check_port(self, num):
    #     """
    #     检查随机生成的端口是否被占
    #     :param num:         循环次数,int类型
    #     :return:            端口数组
    #     """
    #     now_port = []
    #     for index, value in enumerate(self.get_port(num)):
    #         if self.is_free(value):
    #             now_port.append(value)
    #         else:
    #             now_port.append(random.randint(4700, 4900))
    #     return now_port
    #
    # def port_get(self):
    #     """
    #     获取devices.yaml中的端口号
    #     :return:            端口数组
    #     """
    #     devices_data, port_list = self.__yaml.get_yaml(), []
    #     for i in range(0, len(devices_data['devices'])):
    #         port_list.append(devices_data['devices'][i]['port'])
    #     return port_list
    #
    # def port_inspect(self):
    #     """
    #     如果devices.yaml中端口号，已经被占用则重新随机生成一个端口号
    #     :return:            端口数组
    #     """
    #     now_port = []
    #     for value in self.port_get():
    #         if self.is_free(value):
    #             now_port.append(value)
    #         else:
    #             now_port.append(random.randint(4700, 4900))
    #     return now_port


    # def wireless_connection(self, port='8888'):
    #     # Specify the android device port number and connect IP + port to enable remote links
    #     flag = self.check_devices()
    #     device_ip = self.__device_ip
    #     try:
    #         if flag:
    #             give_ip = self.adb_arguments('tcpip %s' % port)[0]
    #             port_flag = str(give_ip).strip('\n')[str(give_ip).strip('\n').find(':') + len(':'):].strip()
    #             if port_flag == port:
    #                 connect_context = self.adb_arguments('connect %s:%s' % (device_ip, port))
    #                 if connect_context < 2:
    #                     tcp_ip = str(connect_context[0]).strip('\t\n')
    #                     if tcp_ip[tcp_ip.find('to') + len('to'):] == str(device_ip) + str(port):
    #                         return True
    #     except Exception as error:
    #         print('\033[1;31;0m %s\033[0m' % error)
