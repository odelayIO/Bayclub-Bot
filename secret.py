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

# Enter Bayclub Username and Password below
_USER_NAME = 'USERNAME'
_USER_PASS = 'PASSWORD'

