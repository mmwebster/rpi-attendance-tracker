# rpi-attendance-tracker
Lab/Class Attendance Tracker using a Raspberry Pi w/ a Magstripe card reader and other peripherals

# Setup (general)
* `git clone git@github.com:mmwebster/rpi-attendance-tracker.git --recursive`
* `cd rpi-attendance-tracker`
* `python main.py` // for temporary use
* `sudo apt-get install nodejs npm`
* `npm install -g pm2`
* `pm2 start main.py --interpreter=python3` // for production use

# todo
Add instructions for daemonizing the program
