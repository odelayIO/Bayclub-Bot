# Bayclub-Bot

I'm not proud of using my engineering skills to cheat the system, but I'm over 40 years old and need to workout to stay healthy.



## System Configuration

The Bayclub-Bot is designed to run on a Linux operating system to take advantage of CRON jobs and Chrome webbrowser.  One can update the script and setup to operate on Windows.  

## Python Script

The script uses `selenium` to automate the booking for the Ignite class at the El Segundo location.  This script is very stupid, and just clicks on the buttons that is current on the Bayclub webpage.  So if the class order changes, then the script will fail, since it assumes each day during booking will have the same number of classes on the page.  This is due to the indexing of the classes on the webpage.  Please feel free to update the script to search for the work "ignite", then click the button for booking.

Install `selenium`:

```bash
pip3 install selenium
```



## Installing Chromedriver

The `chromedriver` will need to be installed on the Linux system:

Download the chromedriver: https://chromedriver.chromium.org/downloads

Select the version for the Chrome version installed on the system.  Then you will need to copy into the `/usr/bin` folder

```bash
sudo cp chromedriver /usr/bin/.
```



## Setting up Cron Job

All classes can be booked 3 days out from the day.  Therefore the `cron` job will start just before 7am, and execute the script which will set a timer to wait for 3 seconds after 7am (e.g. 7:00:03).  

Execute the following command on the terminal:

```bash
crontab -e
```

Then copy the following three lines into the crontab file:

```bash
59 6 * * 2 export DISPLAY=:0 && cd /home/sdr/workspace/bayclub-bot && /usr/bin/python3 bayclub-bot_Book_Ignite_Class.py > bayclub-cron.log 2>&1
59 6 * * 5 export DISPLAY=:0 && cd /home/sdr/workspace/bayclub-bot && /usr/bin/python3 bayclub-bot_Book_Ignite_Class.py > bayclub-cron.log 2>&1
59 6 * * 7 export DISPLAY=:0 && cd /home/sdr/workspace/bayclub-bot && /usr/bin/python3 bayclub-bot_Book_Ignite_Class.py > bayclub-cron.log 2>&1

```



## Configure `bayclub-bot_Book_Ignite_Class.py` Bot

The following parameters will need to be udpated with the user name and password in the script.  Yeah, I said this script is stupid. Update `_USER_NAME` and `_USER_PASS` with the login for Bayclub.

```python
_USER_NAME      = 'your-user-name'
_USER_PASS      = 'your-password'
```

