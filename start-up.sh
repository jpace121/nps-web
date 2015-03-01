# to be ran everytime at start up.
rfcomm bind /dev/rfcomm0 00:13:43:02:34:2E
echo BB-SPIDEV0 >>  /sys/devices/bone_capemgr.9/slots

hostapd -B ./utils/hostapd.conf
ifconfig wlan0 192.168.0.1

python serve_tornado.py

