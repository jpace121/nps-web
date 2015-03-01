# to be ran everytime at start up.
rfcomm bind /dev/rfcomm0 00:13:43:02:34:2E
echo BB-SPIDEV0 >>  /sys/devices/bone_capemgr.9/slots

ifup wlan0
hostapd -B /root/python-bluetooth/utils/hostapd.conf

python /root/python-bluetooth/serve_tornado.py

