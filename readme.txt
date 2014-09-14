
This project will need the following python packages:

django
south
mysql-python
django-simple-captcha
django-tagging
requests
pil
gdata
djblets

To initialize the database, use the following command:

manage.py syncdb --all

To test it locally, run the following command, wait a bit and open a browser on 127.0.0.1:8000

manage.py runserver 127.0.0.1:8000
