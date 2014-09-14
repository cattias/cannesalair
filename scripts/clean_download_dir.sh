#!/bin/sh

find /home/cal/cannesalair.fr/cannesalair/media/files/todownload/ -type f -name "*.zip" -mtime +30 -exec rm -rf {} \;
