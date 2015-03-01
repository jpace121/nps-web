#!/usr/bin/env sh

mkdir -p /var/cache/swap/
dd if=/dev/zero of=/var/cache/swap/swapfile bs=1M count=1024
chmod 0600 /var/cache/swap/swapfile
mkswap /var/cache/swap/swapfile
swapon /var/cache/swap/swapfile

mv /root/python-bluetooth/utils/fstab /etc/fstab

