#!/bin/bash --
# Disable & stop service, clean up installed file(s)
echo "Stopping service custom-splash-screens"
systemctl disable custom-splash-screens.service
systemctl stop custom-splash-screens.service

echo "Cleaning up files"
rm /etc/systemd/system/custom-splash-screens.service

echo "Reloading systemctl deamon"
systemctl daemon-reload
