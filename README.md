cannesalair
===========

Crontab setup
-------------
MAILTO=

# m h  dom mon dow   command
0 2 * * * /home/cal/cannesalair.fr/cannesalair/scripts/clean_download_dir.sh
#commented because of authent changes ### 0,30 * * * * /home/cal/cannesalair.fr/cannesalair/scripts/upload_to_imgur.sh
0,10,20,30,40,50 * * * * /home/cal/cannesalair.fr/cannesalair/scripts/download_jobs.sh
0 6 * * * /home/cal/cannesalair.fr/cannesalair/scripts/backup.sh ftpback-rbx4-55.ovh.net ks200325.kimsufi.com *****
0,30 * * * * /home/cal/cannesalair.fr/cannesalair/scripts/realign_order.sh

Galeries
--------
http://cannesalair.fr/media/files/

Setup
-----

sudo apt-get install mysql-server
sudo apt-get install git
sudo apt-get install python-virtualenv
sudo apt-get install python-dev libmysqlclient-dev

git clone https://github.com/cattias/cannesalair.git
virtualenv cal
source cal/bin/activate
cd cannesalair
pip install -r requirements.txt
easy_install Djblets==0.6.18



