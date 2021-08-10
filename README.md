# OctoPrint-Tiertime

Octoprint plugin for 3d printers of tiertime.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/zhangximin/OctoPrint-Tiertime/archive/master.zip


## Configuration

Set wandServer websocket address at OctoPrint Plugin Settings.

In octopi, it would be ws://localhost:3333

## Install WandServer

### *[Run in RaspberryPi terminal]*

- wget https://github.com/zhangximin/OctoPrint-Tiertime/releases/download/v0.1.5-alpha/WandServer_0.1.5.zip

- unzip ./WandServer_0.1.5.zip

-  sudo vi /etc/rc.local        [Need password]

#### add this line at the end of file /etc/rc.local *before* the last line of "exit 0"
- /home/pi/WandServer/startup.sh
