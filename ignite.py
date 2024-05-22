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
#
###########################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import logging


class ignite(object):
  '''Functions to book Ignite class at Bayclub'''
  
  def __init__(self, url="https://bayclubconnect.com/classes"):
    self.browser = webdriver.Chrome()
    self.browser.get(url)
    self.wait = WebDriverWait(self.browser,15)


  def login(self,user_name='user_name',user_password='password'):
    # Enter User Name
    username = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='username']")))
    username.send_keys(user_name)

    # Enter User Password
    password = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='password']")))
    password.send_keys(user_password)

    # Click Login button
    login_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,\
        "/html/body/app-root/div/app-login/div/app-login-connect/div[1]/div/div/div/form/button")))
    login_button.click()


  def manually_select_day(self,day="'Mo'"):
    day_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, str("//*[text()="+day+"]"))))
    day_button.click()


  def select_day(self,day_of_week,logging):
    # 1: Today is Tuesday, booking for Friday Class
    if(day_of_week==1): 
      logging.info("Today is Tuesday, Booking Friday Ignite Class...")  
      day_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Fr']")))

    # 4: Today is Friday, booking for Monday Ignite Class
    elif(day_of_week==4): 
      logging.info("Today is Friday, Booking Monday Ignite Class...")  
      day_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Mo']")))

    # 6: Today is Sunday, booking for Wednesday Ignite Class
    elif(day_of_week==6): 
      logging.info("Today is Sunday, Booking Wednesday Ignite Class...")  
      day_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='We']")))
    else:
      logging.info("ERROR: CRON Executed on a day that is NOT expected...")
      day_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Sa']")))
    # Click on day to schedule
    day_button.click()


  def select_ignite(self):
    ignite_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,\
        "//*[text()[contains(.,'IGNITE')]]")))
    ignite_button.click()


  def book_ignite(self):
    book_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,\
        "//*[text()[contains(.,'Book class')]]"))) 
        #"/html/body/app-root/div/app-classes-shell/app-classes-details/div/div/app-book-class-details/app-class-details/div/div[2]/div[1]/div/div[4]/button"))) # New link
        #"/html/body/app-root/div/app-classes-shell/app-classes-details/div/div/app-book-class-details/app-class-details/div/div[1]/div[1]/div[6]/button")))  # Old link
    book_button.click()


  def add_to_waitlist_ignite(self):
    waitlist_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,\
        "//*[text()[contains(.,'Add to waitlist')]]")))
        #"/html/body/app-root/div/app-classes-shell/app-classes-details/div/div/app-add-to-wait-list-details/app-class-details/div/div[2]/div[1]/div/div[4]/button"
        #"/html/body/app-root/div/app-classes-shell/app-classes-details/div/div/app-add-to-wait-list-details/app-class-details/div/div[1]/div[1]/div[6]/button")))
    waitlist_button.click()


  def confirm_ignite(self):
    confirm_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,\
        "/html/body/modal-container/div/div/app-universal-confirmation-modal/div[2]/div/div/div[4]/div/button[1]/span")))
        #"//*[text()[contains(.,'CONFIRM BOOKING')]]")))
    confirm_button.click()

  def close(self):
    self.browser.close()

  def save_screenshot(self,fn='screen.png',en=True,dly=0):
    if(en):
      time.sleep(dly)
      self.browser.save_screenshot(fn)
