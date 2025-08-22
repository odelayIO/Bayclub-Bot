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
import ignite
import secret

# -----------------------------------------------------------
#   Parameters
# -----------------------------------------------------------
_USER_NAME      = secret._USER_NAME
_USER_PASS      = secret._USER_PASS

_DELAY_SEC      = 10
_CLASS_TIME_HR  = 7  # Hours in 24hr Time
_CLASS_TIME_MIN = 0  # Minutes in 24hr Time

_DEBUG_MODE     = False
_SCREEN_CAP_EN  = True
_SCREEN_CAP_DLY = 3 # seconds to delay before taking screen capture
_BASE_DIR       = '/home/sdr/workspace/bayclub-bot/'
_LOG_FILE_NAME  = '/home/sdr/workspace/bayclub-bot/baybot.log'
_URL            = 'https://bayclubconnect.com/classes'

_CLASS_TIME     = _CLASS_TIME_HR*100+_CLASS_TIME_MIN

# -----------------------------------------------------------
#   Configure Logging
# -----------------------------------------------------------
logging.basicConfig(filename=_LOG_FILE_NAME, filemode='a',level=logging.INFO,\
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# -----------------------------------------------------------
#   Open Chrome and go to website
# -----------------------------------------------------------
logging.info("Opening Chrome...")
chrome = ignite.ignite(url=_URL)
logging.info("Chrome Opened.")


# -----------------------------------------------------------
#   Setting timer to sleep for exact seconds
# -----------------------------------------------------------
t = datetime.datetime.today()
f = datetime.datetime(t.year,t.month,t.day,_CLASS_TIME_HR,_CLASS_TIME_MIN,_DELAY_SEC)  # 7am Class
day_of_week = f.weekday()  # 6:Sunday, 1:Tuesday, 4:Friday
if(not _DEBUG_MODE):
  logging.info("Auto Booking with Delay...")
  logging.info("  Current Time         : " + str(t))
  logging.info("  Booking Time         : " + str(f))
  s = (f-t).total_seconds()
  logging.info("  Seconds to Booking   : " + str(s))
  
  logging.info("Sleeping for " + str(s) + "seconds...")
  if(s>0):
    time.sleep(s)
  else:
    logging.info("ERROR: Time Delay was negative number...")

else:
  # Used for testing...
  logging.info("************ Debug Mode ********************")


# -----------------------------------------------------------
#   Log into system
# -----------------------------------------------------------
logging.info("Logging into Bayclub...")
chrome.login(user_name=_USER_NAME,user_password=_USER_PASS)
logging.info("Login to Bayclub Done.")

chrome.save_screenshot(fn=str(_BASE_DIR +'1_after_login.png'),\
    en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)



# -----------------------------------------------------------
#   Select Day to book (always 3 days from today)
# -----------------------------------------------------------
logging.info("Selecting day based on what is today...")
if(not _DEBUG_MODE):
  chrome.select_day(day_of_week=day_of_week,logging=logging)
  chrome.save_screenshot(fn=str(_BASE_DIR + '2_after_clicking_on_day_button.png'),\
      en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)
else:
  chrome.manually_select_day(day="'Mo'")
  chrome.save_screenshot(fn=str(_BASE_DIR + '2_after_clicking_on_day_button.png'),\
      en=True,dly=_SCREEN_CAP_DLY)

# -----------------------------------------------------------
#   Book Ignite and confirm
# -----------------------------------------------------------
# This command will select the first Ignite class offered on that day
logging.info('Clicking on Ignite Button...')
chrome.select_ignite(day_of_week=day_of_week, time_of_week="7:00",meridiem="AM")
chrome.save_screenshot(fn=str(_BASE_DIR + '3_after_clicking_on_ignite_button.png'),en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)


if(not _DEBUG_MODE):
  # Click on the book button, if fails, then add to waitlist
  logging.info('Clicking on Book Button...')
  try:
    chrome.save_screenshot(fn=str(_BASE_DIR + '4-1_Clicking_on_book_button.png'),en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)
    chrome.book_ignite() 
    logging.info('Ignite class has spots open, and booked class...')
  except:
    chrome.save_screenshot(fn=str(_BASE_DIR + '4-1_Clicking_on_Add_to_waitlist.png'),en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)
    chrome.add_to_waitlist_ignite() 
    logging.info('Ignite class is full, and added to waitlist...')

  chrome.save_screenshot(fn=str(_BASE_DIR + '4-2_after_clicking_on_book_button.png'),en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)
  
  # Click on the confirmation button, should be in the same location for all classes
  logging.info('Clicking on Confirm Button...')
  chrome.confirm_ignite() 
  chrome.save_screenshot(fn=str(_BASE_DIR + '5_after_clicking_on_confirm_button.png'),en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)

# -----------------------------------------------------------
#   Close Chrome
# -----------------------------------------------------------
logging.info("Closing Chrome in 10 seconds...")
time.sleep(10)
chrome.save_screenshot(fn=str(_BASE_DIR + '6_just_before_exiting_bot.png'),\
    en=_SCREEN_CAP_EN,dly=_SCREEN_CAP_DLY)
chrome.close()
logging.info("Booked Ignite Class\n\n\n")
