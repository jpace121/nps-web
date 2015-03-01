# Instruction for set-up.
# This script should be ran after a reinstall of the operating 
# system. It does not need to be ran everytime. To start the server everytime,
# use ../start-up.sh.

# Assumes starting with default Debian Install from:
# bone-debian-7.8-lxde-4gb-armhf-2015-03-01-4gb.img
# and that you have internet to grab software with apt.


echo '==> Install Adafruit-BBIO and essentials.'
#From adafruit guide
ntpdate pool.ntp.org
apt-get update
apt-get install -y build-essential python-dev python-setuptools python-pip python-smbus 
pip install Adafruit_BBIO
pip install spidev

apt-get install -y zip # for downloads.html
apt-get install -y python-matplotlib

echo '==> Install python dependencies.' 
pip install virtualenv
pip install flask
pip install tornado
pip install subprocess32

echo '==> Installed device tree overlay.'
cp ./BB-SPIDEV0-00A0.dtbo /lib/firmware/.

ehco '==> Set up Bluetooth'
apt-get install -y bluez-utils bluez # these aren't neccessarily neccessary
#bluez-utils is buggy, bluez is already installed (?)
#http://blog.sumostyle.net/2009/11/ubuntu-tethering-via-bluetooth-pan/

echo '==> Bind the handset to the serial port.'
rfcomm bind /dev/rfcomm0 00:13:43:02:34:2E

echo '==> Set up wifi AP.'
#http://andrewmichaelsmith.com/2013/08/raspberry-pi-wi-fi-honeypot/
#Hostapd does not contain correct driver, hostapd must be compiled.
# Instructions: https://github.com/pritambaral/hostapd-rtl871xdrv
# the binaries live in ../utils for our use.
apt-get install -y hostapd dnsmasq # dnsmasq already installed for apache?
cp ./hostapd.conf /etc/hostapd/hostapd.conf
cp ./hostapd.init /etc/init.d/hostapd
cp hostapd /usr/sbin/hostapd # hack, b/c the above stuff didn't work...
cp interfaces /etc/network/interfaces
cp dnsmasq.conf /etc/dnsmasq.conf
sudo update-rc.d hostapd defaults
sudo update-rc.d dnsmasq defaults
cp dnsmasq.default /etc/default/dnsmasq
chmod +x ../start-up.sh # probably redudant
cp ./rc.local /etc/rc.local

echo '==> Set up swap'
sh ./addswap.sh
