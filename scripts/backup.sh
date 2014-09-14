#!/bin/sh

FILE="backup_cal_$(date +%Y%m%d).tar.gz"


HOST=$1
USER=$2
PASSWORD=$3

mkdir -p /tmp/cal
cd /tmp/cal
rm -rf dump 2>>/dev/null

mysqldump --host=localhost --port=3406 --user=cal_write --password='0.Kl&db&20ll!@' --opt --complete-insert --compress --result-file=dump cannesalair_db
tar -czf $FILE dump

ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWORD
cd cal
put $FILE
quit
END_SCRIPT

