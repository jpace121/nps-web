# to be ran everytime at start up.
rfcomm bind /dev/rfcomm0 00:13:43:02:34:2E
echo BB-SPIDEV0 >>  /sys/devices/bone_capemgr.9/slots

./utils/hostapd -B ./utils/hostapd.conf

python serve_tornado.py

