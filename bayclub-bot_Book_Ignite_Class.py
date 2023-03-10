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
#      10FEB2023     Fixed day of week bug, and removed 800 time booking
#      11MAR2023     Search for "IGNITE" class for the day of booking, and added logging
#
#
###########################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import logging

# -----------------------------------------------------------
#   Parameters
# -----------------------------------------------------------
_USER_NAME      = 'your_user_name'
_USER_PASS      = 'your_password'

_ENABLE_TIMER   = True
_DELAY_SEC      = 0
_CLASS_TIME_HR  = 7  # Hours in 24hr Time
_CLASS_TIME_MIN = 0  # Minutes in 24hr Time

_DEBUG_MODE     = False
_LOG_FILE_NAME  = '/home/sdr/workspace/bayclub-bot/baybot.log'

_CLASS_TIME     = _CLASS_TIME_HR*100+_CLASS_TIME_MIN

# -----------------------------------------------------------
#   Configure Logging
# -----------------------------------------------------------
logging.basicConfig(filename=_LOG_FILE_NAME, filemode='a',level=logging.INFO,\
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# -----------------------------------------------------------
#   Setting timer to sleep for exact seconds
# -----------------------------------------------------------
if(_ENABLE_TIMER):
  t = datetime.datetime.today()
  f = datetime.datetime(t.year,t.month,t.day,_CLASS_TIME_HR,_CLASS_TIME_MIN,_DELAY_SEC)  # 7am Class
  day_of_week = f.weekday()  # 6:Sunday, 1:Tuesday, 4:Friday
  logging.info("Auto Booking with Delay...")
  logging.info("  Current Time         : " + str(t))
  logging.info("  Booking Time         : " + str(f))
  s = (f-t).total_seconds()
  logging.info("  Seconds to Booking   : " + str(s))
  
  logging.info("Sleeping for " + str(s) + "seconds...")
  time.sleep(s)
else:
  # Used for testing...
  _DEBUG_MODE = True
  day_of_week = 4  # 6:Sunday, 1:Tuesday, 4:Friday
  logging.info("Auto Booking Now...")


# -----------------------------------------------------------
#   Open Chrome and go to website
# -----------------------------------------------------------
browser = webdriver.Chrome()
browser.get(('https://bayclubconnect.com/classes'))

wait = WebDriverWait(browser,10)
logging.info("Opening Chrome...")


# -----------------------------------------------------------
#   Log into system
# -----------------------------------------------------------
# Enter User Name    
username = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='username']")))
username.send_keys(_USER_NAME)


# Enter User Password
password = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='password']")))
password.send_keys(_USER_PASS)

# Click Login button
login_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/app-login-connect/div[1]/div/div/div/form/button")))
login_button.click()
logging.info("Logged into Bayclub...")


# -----------------------------------------------------------
#   Select Day to book (always 3 days from today)
# -----------------------------------------------------------
class_day = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/div[1]/div/app-classes-filters/div/form/div[4]/div/app-date-slider/div/div[2]/gallery/gallery-core/div/gallery-slider/div/div/gallery-item[1]/div/div/div[4]/div[1]")))
class_day.click()
logging.info("Selected day of class (3 days from today)...")

# This will select a requested day
#    day_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Tu']")))
#    day_button.click()
#    logging.info('Clicking on Tuesday Button...')



# -----------------------------------------------------------
#   Book Ignite and confirm
# -----------------------------------------------------------

# This command will select the first Ignite class offered on that day
ignite_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='IGNITE']")))
ignite_button.click()
logging.info('Clicking on Ignite Button...')

# Click on the book button, should be in the same location for all classes
book_button = wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/app-root/div/app-classes-shell/app-classes-details/div/div/app-book-class-details/app-class-details/div[1]/div[1]/div[6]/button")))
book_button.click()
logging.info('Clicking on Book Button...')

# Click on the confirmation button, should be in the same location for all classes
confirm_button = wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/modal-container/div/div/app-universal-confirmation-modal/div[2]/div/div/div[4]/div/button[1]/span")))
confirm_button.click()
logging.info('Clicking on Confirm Button...')



# -----------------------------------------------------------
#   Close Chrome
# -----------------------------------------------------------
logging.info("Closing Chrome in 10 seconds...")
time.sleep(10)
browser.close()
logging.info("Booked Ignite Class\n\n\n")
