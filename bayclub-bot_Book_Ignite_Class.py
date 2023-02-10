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
#
###########################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# -----------------------------------------------------------
#   Parameters
# -----------------------------------------------------------
_USER_NAME      = 'your_user_name'
_USER_PASS      = 'your_password'

_DELAY          = 0.00
_ENABLE_TIMER   = True
_CLASS_TIME_HR  = 7  # Hours in 24hr Time
_CLASS_TIME_MIN = 0  # Minutes in 24hr Time

_DEBUG_MODE     = False

_CLASS_TIME     = _CLASS_TIME_HR*100+_CLASS_TIME_MIN


# -----------------------------------------------------------
#   Setting timer to sleep for exact seconds
# -----------------------------------------------------------
if(_ENABLE_TIMER):
  t = datetime.datetime.today()
  f = datetime.datetime(t.year,t.month,t.day,_CLASS_TIME_HR,_CLASS_TIME_MIN,3)  # 7am Class
  day_of_week = f.weekday()  # 6:Sunday, 1:Tuesday, 4:Friday
  print("Auto Booking with Delay...")
  print("  Current Time         : " + str(t))
  print("  Booking Time         : " + str(f))
  s = (f-t).total_seconds()
  print("  Seconds to Booking   : " + str(s))
  
  print("Sleeping for " + str(s) + "seconds...")
  time.sleep(s)
else:
  # Used for testing...
  _DEBUG_MODE = True
  day_of_week = 4  # 6:Sunday, 1:Tuesday, 4:Friday
  print("Auto Booking Now...")


# -----------------------------------------------------------
#   Open Chrome and go to website
# -----------------------------------------------------------
browser = webdriver.Chrome()
browser.get(('https://bayclubconnect.com/classes'))

wait = WebDriverWait(browser,10)
print("Opening Chrome...")


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
time.sleep(_DELAY)
print("Logged into Bayclub...")


# -----------------------------------------------------------
#   Select Day to book (always 3 days from today)
# -----------------------------------------------------------
class_day = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/div[1]/div/app-classes-filters/div/form/div[4]/div/app-date-slider/div/div[2]/gallery/gallery-core/div/gallery-slider/div/div/gallery-item[1]/div/div/div[4]/div[1]")))
class_day.click()
time.sleep(_DELAY)
print("Selected Day...")


# -----------------------------------------------------------
#   Book Ignite and confirm
# -----------------------------------------------------------
# 7am Class
if(_CLASS_TIME == 700):
  # 1: Today is Tuesday, booking for Friday Class
  if(day_of_week==1): 
    print('Today is Tuesday, Booking Friday Ignite Class...')  
    book_ignite = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/app-classes-list/div/div[3]/app-classes-can-book-item/app-class-list-item/div/div[1]/div[5]/div")))

  # 4: Today is Friday, booking for Monday Ignite Class
  elif(day_of_week==4): 
    print('Today is Friday, Booking Monday Ignite Class...')  
    book_ignite = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/app-classes-list/div/div[4]/app-classes-can-book-item/app-class-list-item/div/div[1]/div[5]/div")))

  # 6: Today is Sunday, booking for Wednesday Ignite Class
  elif(day_of_week==6): 
    print('Today is Sunday, Booking Wednesday Ignite Class...')  
    book_ignite = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/app-classes-list/div/div[3]/app-classes-can-book-item/app-class-list-item/div/div[1]/div[5]/div")))
  else:
    print('ERROR: CRON Executed on a day that is NOT expected...')
    book_ignite = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-classes-shell/app-classes/div/app-classes-list/div/div[3]/app-classes-can-book-item/app-class-list-item/div/div[1]/div[5]/div")))


if(_DEBUG_MODE):
  print('INFO: Debug Mode')
else:
  # Confirm Booking
  book_ignite.click()
  time.sleep(_DELAY)
  
  confirm = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/modal-container/div/div/app-universal-confirmation-modal/div[2]/div/div/div[4]/div/button[1]")))
  confirm.click()
  time.sleep(_DELAY)


# -----------------------------------------------------------
#   Close Chrome
# -----------------------------------------------------------
time.sleep(10)
browser.close()
print("Booked Ignite Class")


