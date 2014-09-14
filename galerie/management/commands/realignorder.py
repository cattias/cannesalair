from django.core.management.base import BaseCommand
import sys
from galerie.models import DownloadJob, Galerie
import logging
import time
import os
from django.conf import settings
from zipfile import ZipFile
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from core.mail import internal_sendmail
import urllib2
from optparse import make_option

class Command(BaseCommand):

    help = 'Realign Photos order'
    stdout = sys.stdout
    option_list = BaseCommand.option_list + (
        make_option('--loglevel',
            dest='loglevel',
            default="ERROR",
            help='Log Level'),
        )

    def handle(self, *args, **options):
        """Does the job."""
        # create logger with 'uploader'
        logger = logging.getLogger('order')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('order.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        if options.get("loglevel") == "ERROR":
            ch.setLevel(logging.ERROR)
        if options.get("loglevel") == "INFO":
            ch.setLevel(logging.INFO)
        if options.get("loglevel") == "WARN":
            ch.setLevel(logging.WARN)
        if options.get("loglevel") == "DEBUG":
            ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        # logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("###### Starting order realignment ######")
        for galerie in Galerie.objects.all():
            logger.info("    => Working on galerie %s" % galerie)
            i = 1
            for photo in galerie.photos_set.all().order_by("ordre"):
                logger.info("        => Working on photo nb %s : %s" % (i, photo))
                photo.ordre = i
                photo.save()
                i = i + 1
        logger.info("###### Order realignment done. ######")
