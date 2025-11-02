#!/usr/bin/python3


#############################################################################################
#############################################################################################
#
#   The MIT License (MIT)
#   
#   Copyright (c) 2023 http://odelay.io 
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#   
#   Contact : <everett@odelay.io>
#  
#   Description : Bayclub Bot for booking Ignite Class.  See README.md for instructions.
#
#   Version History:
#   
#       Date        Description
#     -----------   -----------------------------------------------------------------------
#      07FEB2023     Original Creation
#      08FEB2023     Added weekday check for M/W/F scheduling
#      10MAR2023     Fixed day of week bug, and removed 800 time booking
#      15MAR2023     Search for text that contains 'IGNITE', so 'IGNITE ' works
#      21APR2023     Created Ignite Class  
#      20OCT2025     Created Resilient Waiter Class
#
###########################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

import time
import datetime
import logging
import os


#################################################################################################
# Configure file-based logging only (no console output)
#################################################################################################
_LOG_FILE_NAME = "/home/sdr/workspace/bayclub-bot/ignite.log"
logging.basicConfig(filename=_LOG_FILE_NAME, filemode='a',level=logging.INFO,\
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


#################################################################################################
# Resilient Waiter Class
#################################################################################################

class ResilientWaiter:
    """
    ResilientWaiter retries Selenium waits with exponential backoff
    and optional page refresh on timeout.
    """

    def __init__(self, driver, base_wait=10, max_attempts=4, refresh_on_fail=True):
        self.driver = driver
        self.base_wait = base_wait
        self.max_attempts = max_attempts
        self.refresh_on_fail = refresh_on_fail

    def _wait_for_page_ready(self, timeout=None):
        timeout = timeout or self.base_wait
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _resilient_wait(self, condition, description="condition"):
        for attempt in range(self.max_attempts):
            wait_time = self.base_wait * (2 ** attempt)
            try:
                logging.info(f"Attempt {attempt + 1}: waiting up to {wait_time}s for {description}...")
                WebDriverWait(self.driver, wait_time).until(condition)
                logging.info(f"Success: {description} satisfied.")
                return True
            except TimeoutException:
                logging.warning(f"Timeout after {wait_time}s on attempt {attempt + 1} for {description}.")
                if self.refresh_on_fail:
                    try:
                        logging.info("Refreshing page and retrying...")
                        self.driver.refresh()
                        self._wait_for_page_ready(timeout=self.base_wait)
                    except WebDriverException as e:
                        logging.error(f"Refresh failed: {e}")
            except WebDriverException as e:
                logging.error(f"WebDriver error during wait: {e}")
                time.sleep(3)

        logging.error(f"Failed to satisfy {description} after {self.max_attempts} attempts.")
        return False

    # ---- Public helpers ----
    def wait_for_page_ready(self, timeout=None):
        """Wait until document.readyState == 'complete'."""
        return self._resilient_wait(
            lambda d: d.execute_script("return document.readyState") == "complete",
            description="page readiness"
        )

    def wait_for_element(self, by, selector):
        """Wait until a specific element is present in the DOM."""
        condition = EC.presence_of_element_located((by, selector))
        return self._resilient_wait(condition, description=f"element {selector}")

    def wait_for_visible_element(self, by, selector):
        """Wait until a specific element is visible (like EC.visibility_of_element_located)."""
        condition = EC.visibility_of_element_located((by, selector))
        return self._resilient_wait(condition, description=f"visible element {selector}")

    def wait_for_clickable(self, by, selector):
        """Wait until a specific element is clickable."""
        condition = EC.element_to_be_clickable((by, selector))
        return self._resilient_wait(condition, description=f"clickable element {selector}")


#################################################################################################
# Ignite Class
#################################################################################################

class ignite(object):
  '''Functions to book Ignite class at Bayclub'''

  def __init__(self, url="https://bayclubconnect.com/classes"):
    self.browser = webdriver.Chrome('/usr/bin/chromedriver')
    self.browser.get(url)

    # Use ResilientWaiter instead of a static 30s wait
    self.waiter = ResilientWaiter(self.browser, base_wait=10, max_attempts=4, refresh_on_fail=True)
    self.waiter.wait_for_page_ready()

  def login(self,user_name='user_name',user_password='password'):
    username_xpath = "//*[@id='username']"
    password_xpath = "//*[@id='password']"
    button_xpath = "/html/body/app-root/div/app-login/div/app-login-connect/div[1]/div/div/div/form/button"

    self.waiter.wait_for_visible_element(By.XPATH, username_xpath)
    username = self.browser.find_element(By.XPATH, username_xpath)
    username.send_keys(user_name)

    self.waiter.wait_for_visible_element(By.XPATH, password_xpath)
    password = self.browser.find_element(By.XPATH, password_xpath)
    password.send_keys(user_password)

    self.waiter.wait_for_clickable(By.XPATH, button_xpath)
    login_button = self.browser.find_element(By.XPATH, button_xpath)
    login_button.click()

  def manually_select_day(self,day="'Mo'"):
    day_xpath = f"//*[text()={day}]"
    self.waiter.wait_for_visible_element(By.XPATH, day_xpath)
    self.browser.find_element(By.XPATH, day_xpath).click()

  def select_day(self,day_of_week):
    if(day_of_week==1): 
      logging.info("Today is Tuesday, Booking Friday Ignite Class...")  
      day_xpath = "//*[text()='Fr']"
    elif(day_of_week==4): 
      logging.info("Today is Friday, Booking Monday Ignite Class...")  
      day_xpath = "//*[text()='Mo']"
    elif(day_of_week==6): 
      logging.info("Today is Sunday, Booking Wednesday Ignite Class...")  
      day_xpath = "//*[text()='We']"
    else:
      logging.info("ERROR: CRON Executed on a day that is NOT expected...")
      day_xpath = "//*[text()='Sa']"

    self.waiter.wait_for_clickable(By.XPATH, day_xpath)
    self.browser.find_element(By.XPATH, day_xpath).click()

  def select_ignite(self,day_of_week: int, time_of_week: str = "7:00", meridiem: str = "AM"):
    #
    # Selects the IGNITE class for the given day of the week and time.
    # 
    # Args:
    #    day_of_week (int): Python weekday (0=Monday, 6=Sunday).
    #    time_of_week (str): The time string to look for, e.g. "7:00" or "6:30".
    #    meridiem (str): AM/PM
    #

    ignite_xpath = f"""
    //div[contains(@class,'col-2')
     and contains(normalize-space(),'{time_of_week}')
     and contains(normalize-space(),'{meridiem}')]
    /parent::div
    //div[@class='size-16 text-uppercase' 
         and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ignite')]
    """

    self.waiter.wait_for_clickable(By.XPATH, ignite_xpath)
    ignite_button = self.browser.find_element(By.XPATH, ignite_xpath)
    ignite_button.click()

  def book_ignite(self):
    book_xpath = "//*[text()[contains(.,'Book class')]]"
    self.waiter.wait_for_visible_element(By.XPATH, book_xpath)
    self.browser.find_element(By.XPATH, book_xpath).click()

  def add_to_waitlist_ignite(self):
    waitlist_xpath = "//*[text()[contains(.,'Add to waitlist')]]"
    self.waiter.wait_for_visible_element(By.XPATH, waitlist_xpath)
    self.browser.find_element(By.XPATH, waitlist_xpath).click()

  def confirm_ignite(self):
    confirm_xpath = "/html/body/modal-container/div/div/app-universal-confirmation-modal/div[2]/div/div/div[4]/div/button[1]/span"
    self.waiter.wait_for_clickable(By.XPATH, confirm_xpath)
    self.browser.find_element(By.XPATH, confirm_xpath).click()

  def close(self):
    self.browser.close()

  def save_screenshot(self,fn='screen.png',en=True,dly=0):
    if(en):
      time.sleep(dly)
      self.browser.save_screenshot(fn)

