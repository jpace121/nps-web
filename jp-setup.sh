# Instruction for set-up
# Assumes starting with default Debian Install from:
# bone-debian-7.8-lxde-4gb-armhf-2015-03-01-4gb.img

# Needs internet access to grab all the stuff from apt
sudo -u  root  sh << EOF

#From adafruit guide
ntpdate pool.ntp.org
apt-get update
apt-get install -y build-essential python-dev python-setuptools python-pip python-smbus 
pip install Adafruit_BBIO
pip install spidev

#B/c we ship python apps
pip install virtualenv

#Bluetooth
apt-get install bluez-utils bluez # these aren't neccessarily neccessary
#bluez-utils is buggy, bluez is already installed (?)
#http://blog.sumostyle.net/2009/11/ubuntu-tethering-via-bluetooth-pan/

EOF

