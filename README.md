# Bayclub-Bot

I'm not proud of using my engineering skills to cheat the system, but I'm over 40 years old and need to workout to stay healthy.

This Python script will automatically register for the Ignite class at 7am for Monday, Wednesday, and Friday.  The Bayclub mobile app is just a website, so you can access the same features from a desktop computer.



### Assumptions

This is a list of assumptions:

- The default location is El Segundo, and you profile has El Segundo as the default location when booking a class.
- Only support Linux (e.g. Ubuntu) with `cron` for scheduling the time to book the Ignite class.
- Only supports Chrome webbrowser driver.



## System Configuration

The Bayclub-Bot is designed to run on a Linux operating system to take advantage of CRON jobs and Chrome webbrowser.  One can update the script and setup to operate on Windows.  

## Python Script

The script uses `selenium` to automate the booking for the Ignite class at the El Segundo location.  This script is very stupid, and just clicks on the buttons that is current on the Bayclub webpage.  So if the class order changes, then the script will fail, since it assumes each day during booking will have the same number of classes on the page.  This is due to the indexing of the classes on the webpage.  Please feel free to update the script to search for the work "ignite", then click the button for booking.

Install `selenium`:

```bash
pip3 install selenium
```



## Installing Chromedriver 

#### General Linux Operating System

The `chromedriver` will need to be installed on the Linux system:

Download the chromedriver: https://chromedriver.chromium.org/downloads

Select the version for the Chrome version installed on the system.  Then you will need to copy into the `/usr/bin` folder

```bash
sudo cp chromedriver /usr/bin/.
```



#### Installing Chromedriver for Raspberrypi

Unfortunately, Google doesn't make `AMR32` (`armv7l`) builds of ChroreDriver anymore. The latest version of `chromedriver-linux32` was released for version [2.33](https://chromedriver.storage.googleapis.com/index.html?path=2.33/)

But there is a solution, people from [the Raspbian project](https://www.raspbian.org/) have compiled chromium-chromedriver version for the `armhf` platform and added it to the repo.

```bash
sudo apt-get install chromium-chromedriver
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

Please note the following for `crontab` to select days:

| Day Of Week | CRONTAB Label |
| ----------- | ------------- |
| Monday      | 1             |
| Tuesday     | 2             |
| Wednesday   | 3             |
| Thursday    | 4             |
| Friday      | 5             |
| Saturday    | 6             |
| Sunday      | 7 (or 0)      |



## Configure `bayclub-bot_Book_Ignite_Class.py` Bot

The following parameters will need to be udpated with the user name and password in the script.  Yeah, I said this script is stupid. Update `_USER_NAME` and `_USER_PASS` with the login for Bayclub.

```python
_USER_NAME      = 'your-user-name'
_USER_PASS      = 'your-password'
```

Please note the `datetime.weekday()` is used to determine the day of the week.  The label is the following:

| Day Of Week | datetime.weekday() Returns |
| ----------- | -------------------------- |
| Monday      | 0                          |
| Tuesday     | 1                          |
| Wednesday   | 2                          |
| Thursday    | 3                          |
| Friday      | 4                          |
| Saturday    | 5                          |
| Sunday      | 6                          |

The bot needs to book on the following days:

| CRONTAB Execute Day:        | Booking for Class that Occurs on:   |
| --------------------------- | ----------------------------------- |
| Sunday (crontab code: `7`)  | Wednesday Class (`day_of_week = 6`) |
| Tuesday (crontab code: `2`) | Friday Class (`day_of_week = 1`)    |
| Friday (crontab code: `5`)  | Monday Class (`day_of_week = 4`)    |

