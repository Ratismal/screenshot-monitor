#!/bin/bash

chmod +x ./monitor.py
cp screenshot-monitor.service /home/deck/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable screenshot-monitor.service
systemctl --user start screenshot-monitor.service
systemctl --user status screenshot-monitor.service
