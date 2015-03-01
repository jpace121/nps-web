#!/usr/bin/sh

# This scipt shoulf be ran everytime at start up.
# The script handles the stuff that must be done everytime at boot.
echo '==> Bind Bluetooth port.'
rfcomm bind /dev/rfcomm0 00:13:43:02:34:2E
echo '==> Set up device tree overlay.'
echo BB-SPIDEV0 >>  /sys/devices/bone_capemgr.9/slots

echo '==> Wifi set up.'
ifup wlan0
service dnsmasq restart
service hostapd restart
#hostapd -B /root/python-bluetooth/utils/hostapd.conf

echo '==> Start server.'
python /root/python-bluetooth/serve_tornado.py &

