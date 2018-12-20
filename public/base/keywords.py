#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  keywords
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# description    :  Mobile device page operation class
# ========================================================
import os
import random
import re
import time
from PIL import ImageDraw, Image
from appium import webdriver
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common import exceptions as Ex
from selenium.webdriver.support.wait import WebDriverWait
from config import parameters
from public.utils import adb
from public.common import logger


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_the_instance'):
            cls._the_instance = object.__new__(cls)
        return cls._the_instance


class BasePage(Singleton):

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.__adb = adb.Adb()
        self.l = logger.Logger()

    def set_again(self, driver: webdriver.Remote):
        """
        Single case mode, when Dr Changes, reset.

        :Args:
         - driver: Create a new driver that will issue commands using the wire protocol.
        """
        self.driver = driver
        self.__adb = adb.Adb()
        self.l = logger.Logger()
        return self

    def wait(self, seconds):
        """
        Sets an implicit wait for an element to be found

        :Args:
         - seconds: Amount of time to wait (in seconds)

        :Usage:
            driver.wait(30)
        """
        start_time = time.time()
        self.driver.implicitly_wait(seconds)
        self.l.get_logger("Recessive waiting {0} seconds, Spend {1} seconds"
                          .format(seconds, time.time()-start_time), "INFO")

    def key_code(self, num):
        """
        Sends a key_code to the device.

        :Args:
         - num: the key_code to be sent to the device, INT TYPE

        :Usage:
            driver.key_code(3)
        """
        start_time = time.time()
        try:
            self.driver.press_keycode(num)
            self.l.get_logger("The physical keyboard number for the operation is {0}, Spend {1} seconds"
                              .format(num, time.time()-start_time), "SUCCESS")
        except Exception:
            self.l.get_logger('The physical keyboard performs an error, Spend {0} seconds'
                              .format(time.time()-start_time), "FAIL")
            raise

    def long_key_code(self, num):
        """
        Long press the physical keyboard

        :Args:
         - num: the key_code to be sent to the device, INT TYPE

        :Usage:
            driver.long_key_code(3)
        """
        start_time = time.time()
        try:
            self.driver.long_press_keycode(num)
            self.l.get_logger("Long press the physical keyboard number is{0}, Spend {1} seconds"
                              .format(num, time.time()-start_time), "SUCCESS")
        except Exception:
            self.l.get_logger("Long press the physical keyboard number is{0}, Spend {1} seconds"
                              .format(num, time.time()-start_time), "FAIL")
            raise

    def key_event(self, arg):
        """
        Mobile keyboard operation event.

        :Args:
         - arg: Select parameters, default HOME,BACK,CAMERA, DICT TYPE

        :Usage:
            driver.key_event('KEYCODE_BACK')
        """
        event_list = {'HOME': 3, 'BACK': 4, 'CAMERA': 27}
        if arg in event_list:
            self.key_code(int(event_list[arg]))

    def find_element(self, *loc):
        """
        Repackage the single element location method

        :Args:
         - loc: Element localizer, TUPLE TYPE

        :Usage:
            driver.find_element(*locator)
        """
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception:
            self.l.get_logger('Please enter the correct targeting elements!', 'FAIL')
            raise

    def save_screenshot_as_picture(self, filename):
        """
        Saves a screenshot of the current window to a PNG image file

        :Args:
         - filename: filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.

        :Usage:
            driver.save_screenshot_as_picture('login')
        """
        start_time = time.time()
        try:
            image = self.driver.get_screenshot_as_file(parameters.document_name('img', filename))
            self.l.get_logger("The screenshot is successful, the name of the picture is {0},  Spend {1} seconds "
                              .format(filename, time.time()-start_time), 'SUCCESS')
            return image
        except Exception:
            self.l.get_logger("Screenshots failed, Spend {0} seconds".format(time.time()-start_time), 'FAIL')
            raise

    def get_latest_picture(self):
        """
        Get the latest screen shot picture.

        :Usage:
            driver.get_latest_picture()
        """
        start_time = time.time()
        try:
            dirs = os.listdir(parameters.document_name('img'))
            if dirs is not None:
                dirs.sort()
                new_image = dirs[-1]
                self.l.get_logger("Get the latest screenshot is {0}, spend {1} seconds"
                                  .format(new_image, time.time()-start_time), 'SUCCESS')
                return new_image
            else:
                self.l.get_logger("The directory {0} is empty".format(dirs), 'FAIL')
        except FileNotFoundError:
            raise

    def find_elements(self, *loc, index=None, find_way='random'):
        """
        Repackage a set of element location methods.

        :Args:
         - loc: Element localizer, TUPLE TYPE
         - index: Element index, INT TYPE DEFAULT NONE
         - find_way: Element Location Method, STR TYPE DEFAULT RANDOM

        :Usage:
            driver.find_elements(1, 'normal', *locator)
        """
        try:
            if find_way == 'random':
                if len(self.driver.find_elements(*loc)) > 0:
                    num = random.randint(1, len(self.driver.find_elements(*loc)))
                    return self.driver.find_elements(*loc)[num]
            else:
                return self.driver.find_elements(*loc)[index]
        except Exception:
            self.l.get_logger('No related elements are found in the interface.', 'FAIL')
            raise

    def elements_click(self, *loc, index):
        """
        Click on one of the set of elements.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - index: Locate a set of element index values, INT TYPE

        :Usage:
            driver.elements.click(*locator, 2)
        """
        start_time = time.time()
        try:
            self.l.get_logger("Click the element <{0} -> {1}>,  Spend {2} seconds"
                              .format(loc[0], loc[1], time.time() - start_time), 'SUCCESS')
            return self.find_elements('normal', *loc)[index].click()
        except Exception:
            self.l.get_logger("Click the element <{0} -> {1}>,  Spend {2} seconds"
                              .format(loc[0], loc[1], time.time() - start_time), 'FAIL')
            raise

    def random_click(self, *loc):
        """
        Random click on one of the elements.

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            driver.random_click(*locator)
        """
        start_time = time.time()
        try:
            self.l.get_logger("Random click the element <{0} -> {1}>, Spend {2} seconds "
                              .format(loc[0], loc[1], time.time() - start_time), 'SUCCESS')
            return self.find_elements(*loc).click()
        except Exception:
            self.l.get_logger("No element found, click failure, Spend {0} seconds"
                              .format(time.time()-start_time), 'FAIL')
            raise

    @staticmethod
    def change_element_name(*loc):
        """
        Element location removes illegal characters for automatic naming of screen shots picture.

        :Args:
        - loc：Element localizer, TUPLE TYPE.

        :Usage:
            driver.change_element_name(*locator)
        """
        if loc[0] in ['link text', 'name']:
            return loc[1]
        else:
            return re.sub('[\/:*?"<>|]', '-', loc[1])

    def red_element(self, *loc):
        """
        [image processing] marking the elements of the current operation with the matrix (red).

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            driver.red_element(*locator)
        """
        element = self.find_element(*loc)
        self.save_screenshot_as_picture(self.change_element_name(*loc))
        box = (element.location["x"], element.location["y"],
               element.location["x"] + element.size["width"],
               element.location["y"] + element.size["height"])
        new_image = os.path.join(parameters.document_name('img'), self.get_latest_picture())
        img = Image.open(new_image)
        draw = ImageDraw.Draw(img)
        draw.rectangle((box[0], box[1], box[2], box[3]), outline='#8B0000')
        return img.save(new_image)

    def get_element_image(self, *loc):
        """
        Just truncate an image of an element and save it to the corresponding file directory.

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            diver.get_element_image(*locator)
        """
        element = self.find_element(*loc)
        self.save_screenshot_as_picture(self.change_element_name(*loc))
        box = (element.location["x"], element.location["y"],
               element.location["x"] + element.size["width"],
               element.location["y"] + element.size["height"])
        new_image = os.path.join(parameters.document_name('img'), self.get_latest_picture())
        img = Image.open(new_image)
        im = img.crop(box)
        return im.save(parameters.document_name('cut_img', self.change_element_name(*loc)))

    def get_text(self, *loc):
        """
        Gets the element text value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            driver.get_text(*locator)
        """
        start_time = time.time()
        try:
            self.red_element(*loc)
            self.l.get_logger("Get the text <{0} -> {1}>, Spend {2} seconds"
                              .format(loc[0], loc[1], time.time() - start_time), 'SUCCESS')
            return self.find_element(*loc).text
        except Exception:
            self.l.get_logger("Gets the element text failed, Spend {0} seconds"
                              .format(time.time()-start_time), 'FAIL')
            raise

    def click(self, *loc):
        """
        Click on the element

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            driver.click(*locator)
        """
        start_time = time.time()
        try:
            self.red_element(*loc)
            self.l.get_logger("Click the element <{0} -> {1}>, Spend {2} seconds"
                              .format(loc[0], loc[1], time.time() - start_time), 'SUCCESS')
            return self.find_element(*loc).click()
        except Exception:
            self.l.get_logger("Element click failure, Spend {0} seconds".format(time.time()-start_time), 'FAIL')
            raise

    def send_keys(self, value, *loc, clear_first=True):
        """
        Text input

        :Args:
         - clear_first: Clean up the contents in the input box, default Boolean value True.
         - loc: Element localizer, TUPLE TYPE.
         - value: The input Element location text value

        :Usage:
            driver.send_keys('13564958080', *locator)
        """
        start_time = time.time()
        try:
            if clear_first:
                self.find_element(*loc).clear()
            self.red_element(*loc)
            self.l.get_logger("Clear and input text to the element <{0} -> {1}> content: {2}, Spend {3} time "
                              .format(loc[0], loc[1], value, time.time() - start_time), 'SUCCESS')
            return self.find_element(*loc).send_keys(value)
        except Exception:
            self.l.get_logger("Element not found, text input failed, Spend {0} seconds"
                              .format(time.time()-start_time), 'FAIL')
            raise

    def get_attribute(self, *loc, attribute):
        """
        Gets the element attribute value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - attribute: Element attributes, STR TYPE.

        :Usage:
            diver.get_attribute(*locator, 'value')
        """
        start_time = time.time()
        try:
            attr = self.find_element(*loc).get_attribute(attribute)
            self.l.get_logger("Gets the attribute {2} of the element <{0} -> {1} >, Spend {3} seconds"
                              .format(loc[0], loc[1], attribute, time.time() - start_time), 'SUCCESS')
            return attr
        except Exception:
            self.l.get_logger("Gets the attribute {2} of the element <{0} -> {1} >, Spend {3} seconds"
                              .format(loc[0], loc[1], attribute, time.time()-start_time), 'FAIL')
            raise

    def text_in_element(self, loc, text, time_out=10):
        """
        Determines whether the expected text value is equal to the actual element text value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - text: Element location text value, STR TYPE.
         - time_out: Wait time, default 10 seconds, INT OR FLOAT TYPE.

        :Usage:
            kw_loc = (By.ID, 'kw')
            driver.text_in_element(kw_loc, '百度')
        """
        start_time = time.time()
        try:
            WebDriverWait(self.driver, time_out, 0.5).until(Ec.text_to_be_present_in_element(loc, text))
            self.l.get_logger('the text: {0} in element <{1} -> {2} >, Spend {3} seconds'
                              .format(text, loc[0], loc[1], time.time()-start_time), 'SUCCESS')
            return True
        except TimeoutError:
            self.l.get_logger('the text: {0} not in element <{1} -> {2} >, Spend {3} seconds'
                              .format(text, loc[0], loc[1], time.time()-start_time), 'FAIL')
            return False

    def sleep(self, seconds):
        """
        Sets an Mandatory wait for an element to be found

        :Args:
         - seconds: Amount of time to wait (in seconds)

        :Usage:
            driver.sleep(10)
        """
        time.sleep(seconds)
        self.l.get_logger("Mandatory waiting {0}".format(seconds), 'INFO')

    def quit(self):
        """
        Close the browser window.

        :Usage:
            driver.quit()
        """
        start_time = time.time()
        self.driver.quit()
        self.l.get_logger('Close all browser Windows, Spend {0} seconds'.format(time.time()-start_time), 'INFO')

    def switch_to_h5(self, *loc):
        """
        Switch to the  H5 interface

        :Args:
         - loc: Element localizer, TUPLE TYPE.

        :Usage:
            driver.switch_h5(*locator)
        """
        start_time = time.time()
        try:
            current_windows = self.driver.current_context
            self.click(*loc)
            self.wait(3)
            all_windows = self.driver.contexts
            if len(all_windows) > 1:
                for handle in all_windows:
                    if handle != current_windows:
                        self.driver.switch_to.context(handle)
                self.l.get_logger('Switch to the H5 interface, Spend {0} seconds'
                                  .format(time.time() - start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('Switch to the H5 interface, Spend {0} seconds'
                              .format(time.time() - start_time), 'FAIL')
            raise

    def switch_to_native(self):
        """
        Switch to the  native page

        :Usage:
            driver.switch_native()
        """
        start_time = time.time()
        try:
            current_windows = self.driver.current_context
            all_windows = self.driver.contexts
            if len(all_windows) > 1:
                for handle in all_windows:
                    if handle != current_windows:
                        self.driver.switch_to.context(handle)
                self.l.get_logger('Switch to the native page, Spend {0} seconds'
                                  .format(time.time() - start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('Switch to the native page, Spend {0} seconds'
                              .format(time.time() - start_time), 'FAIL')
            raise

    def jquery_click(self, css):
        """
        Jquery click event

        :Args:
         - css: CSS locator, STR TYPE.

        :Usage:
            driver.jquery_click('#kw')
        """
        start_time = time.time()
        try:
            script = "${'{0}'}.click()".format(css)
            self.driver.execute_script(script)
            self.l.get_logger("Use Jquery click element: {0}, Spend {1} seconds"
                              .format(css, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger("The Jquery click event execution failed, Spend {0} seconds"
                              .format(time.time()-start_time), 'FAIL')
            raise

    def jquery_send(self, css, value):
        """
        Jquery input event

        :Args:
         - css: CSS locator, STR TYPE.
         - value: The Element locator text input value, STR TYPE.

        :Usage:
            driver.jquery_send('#kw', 'PYTHON')
        """
        start_time = time.time()
        try:
            script = "${'{0}'}.val('{1}')".format(css, value)
            self.driver.execute_script(script)
            self.l.get_logger("Use Jquery input text to the element: {0} content: {1}, Spend {2} seconds"
                              .format(css, value, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger("The Jquery input event execution failed, Spend {0} seconds"
                              .format(time.time()-start_time), 'FAIL')
            raise

    def js(self, script):
        """
        Execute the js script

        :Args:
         - script: JavaScript, STR TYPE.

        :Usage:
            driver.js(document.getElementById('kw').value('test'))
        """
        start_time = time.time()
        try:
            self.driver.execute_script(script)
            self.l.get_logger(" Execute the JS script is {0}, Spend {1} seconds"
                              .format(script, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('JS script execution fails.', 'FAIL')
            raise

    @property
    def get_width(self):
        """
        Get the phone screen width.

        :Usage:
            driver.get_width
        """
        return self.driver.get_window_size()['width']

    @property
    def get_height(self):
        """
        Get the phone screen height.

        :Usage:
            driver.get_height
        """
        return self.driver.get_window_size()['height']

    def swipe_down(self, count=1, timeout=500):
        """
        The phone screen slides down.

        :Args:
         - count: Slide number, INT TYPE.
         - timeout: Slide duration, default 500.

        :Usage:
            driver.swipe_down()
        """
        width, height = self.get_width, self.get_height
        start_time = time.time()
        try:
            while count:
                self.driver.swipe(width*0.5, height*0.25, height*0.75, timeout)
                count -= 1
            self.l.get_logger("The phone screen slides down {0} count, Spend {1}"
                              .format(count, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger("The phone screen slides down {0} count, Spend {1}"
                              .format(count, time.time()-start_time), 'FAIL')
            raise

    def swipe_left(self, count=1, timeout=500):
        """
        The phone screen slides to the left.

        :Args:
         - count: Slide number, INT TYPE.
         - timeout: Side duration, default 500.

        :Usage:
            driver.swipe_left()
        """
        width, height = self.get_width, self.get_height
        start_time = time.time()
        try:
            while count:
                self.driver.swipe(width*0.75, height*0.5, width*0.05, timeout)
                count -= 1
            self.l.get_logger("The phone screen slides left {0} count, Spend {1}"
                              .format(count, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger("The phone screen slides left {0} count, Spend {1}"
                              .format(count, time.time()-start_time), 'FAIL')
            raise

    def reset(self):
        """
        Reset the application

        :Usage:
            driver.reset()
        """
        self.driver.reset()

    def is_select(self, *loc):
        """
        Check whether the control is selected.

        :Args:
         - loc: Element locator, TUPLE TYPE.

        :Usage:
            driver.is_select(*locator)
        """
        start_time = time.time()
        try:
            self.find_element(*loc).is_selected()
            self.l.get_logger('The element <{0} -> {1} > has been selected,Spend {2} seconds'
                              .format(loc[0], loc[1], time.time()-start_time), 'SUCCESS')
            return True
        except (Ex.NoSuchElementException, Ex.ElementNotSelectableException, Ex.TimeoutException):
            self.l.get_logger('The element <{0} -> {1} > has not been selected,Spend {2} seconds'
                              .format(loc[0], loc[1], time.time()-start_time), 'SUCCESS')
            return False

    def element_scroll(self, el_loc, tar_loc):
        """
        ELEMENT SCROLL

        :Args:
         - el_loc: drag locator, TUPLE TYPE.
         - tar_loc: target locator, TUPLE TYPE.

        :Usage:
            driver.element_scroll(*drap_locator, *target_locator)
        """
        start_time = time.time()
        try:
            element = self.find_element(*el_loc)
            target = self.find_element(*tar_loc)
            self.driver.scroll(element, target)
            self.l.get_logger('element <{0} -> {1} > scroll to element <{2} -> {3} >, Spend {4} seconds'
                              .format(el_loc[0], el_loc[1], tar_loc[0], tar_loc[1], time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('element scroll fail,Spend {0} seconds'.format(time.time()-start_time), 'FAIL')
            raise

    def drag_and_drop(self, el_loc, tar_loc):
        """
        Mouse drag and drop event

        :Args:
         - el_loc: drag locator, TUPLE TYPE.
         - tar_loc: target locator, TUPLE TYPE.

        :Usage:
            driver.drag_and_drop(*drap_locator, *target_locator)
        """
        start_time = time.time()
        try:
            element = self.find_element(*el_loc)
            target = self.find_element(*tar_loc)
            self.driver.drag_and_drop(element, target)
            self.l.get_logger('element <{0} -> {1} > move to element <{2} -> {3} >, Spend {4} seconds'
                              .format(el_loc[0], el_loc[1], tar_loc[0], tar_loc[1], time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('drag and drop fail,Spend {0} seconds'.format(time.time()-start_time), 'FAIL')
            raise

    def tap(self, *coordinates, timeout=10):
        """
        Simulate finger click

        :Args:
         - coordinates: coordinates, TUPLE OR LIST TYPE.
         - timeout: Duration,DEFAULT 10.

        :Usage:
            driver.tap([(100,200), (210, 300)])
        """
        start_time = time.time()
        try:
            self.driver.tap(*coordinates, timeout)
            self.l.get_logger('Simulate finger click, Spend {0}'
                              .format(time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger('Simulate finger click failure, Spend {0}'
                              .format(time.time()-start_time), 'FAIL')
            raise

    def background_app(self, timeout=5):
        """
        App background operation

        :Args:
         - timeout: Duration, DEFAULT 5, STR TYPE.

        :Usage:
            driver.background_app(10)
        """
        start_time = time.time()
        try:
            self.driver.background_app(timeout)
            self.l.get_logger("App background operation {0} seconds, Spend {1} seconds"
                              .format(timeout, time.time()-start_time), 'SUCCESS')
        except Exception:
            self.l.get_logger("App background running failure.", 'FAIL')
            raise

    def check_install_app(self, package):
        """
        Check to see if the app is installed.

        :Args:
         - package: app install package, STR TYPE.

        :Usage:
            driver.check_install_app(package)
        """
        start_time = time.time()
        self.driver.is_app_installed(package)
        self.l.get_logger("Installed app {0}, Spend {1} seconds"
                          .format(package, time.time()-start_time), 'INFO')

    def close_app(self):
        """
        Stop app running application

        :Usage:
            driver.close_app()
        """
        start_time = time.time()
        self.driver.close_app()
        self.l.get_logger("Close the app, Spend {0} seconds"
                          .format(time.time()-start_time), 'INFO')

    def shake_device(self):
        """
        Shake the device

        :Usage:
            driver.shake_device()
        """
        start_time = time.time()
        self.driver.shake()
        self.l.get_logger("Shake the driver, Spend {0} seconds"
                          .format(time.time()-start_time), 'INFO')

    def start_toggle_location_services(self):
        """
        Toggle the location services on the device

        :Usage:
            driver.start_toggle_location_services()
        """
        start_time = time.time()
        self.driver.toggle_location_services()
        self.l.get_logger("Toggle the location services on the device"
                          .format(time.time()-start_time), 'INFO')

    def get_page_source(self):
        """
        Gets the source of the current page

        :Usage:
            driver.get_page_source()
        """
        start_time = time.time()
        self.l.get_logger("Gets the source of the current page".format(time.time()-start_time), 'INFO')
        return self.driver.page_source


if __name__ == '__main__':
    pass
