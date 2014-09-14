from django.core.management.base import BaseCommand
import sys
from galerie.models import DownloadJob
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

    help = 'Create zipfiles to download'
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
        logger = logging.getLogger('downloader')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('download.log')
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

        logger.info("###### Starting zip for download creation ######")
        i=0
        job_to_treat = DownloadJob.objects.filter(is_treated=False, is_intreatment=False, is_deleted=False)
        
        nbtotal = job_to_treat.count()
        for job in job_to_treat:
            job.intreatment = True
            job.save()
        for job in job_to_treat:
            try:
                i+=1
                logger.info("%s of %s - Treating Job for email '%s'" % (i, nbtotal, job.email))
                dirname = "%s_%s" % (job.galerie.titre_slug, int(time.time()))
                logger.debug("dirname=" + dirname)
                zipname = dirname+".zip"
                logger.debug("zipname=" + zipname)
                rootpath = os.path.join(settings.TODOWNLOAD_ROOT, dirname)
                logger.debug("rootpath=" + rootpath)
                if not os.path.exists(rootpath):
                    os.makedirs(rootpath)
                zipfilename = os.path.join(settings.TODOWNLOAD_ROOT, zipname)
                logger.debug("zipfilename=" + zipfilename)
                zipfile = ZipFile(zipfilename, "w")
                j = 0
                totalimages = job.images.all().count()
                for image in job.images.all():
                    try:
                        j += 1
                        logger.info("%s of %s - Treating image '%s' for email '%s'" % (j, totalimages, image.filename, job.email))
                        logger.debug("image.filename=" + image.filename)
                        if image.hash:
                            logger.debug("image.hash=" + image.hash)
                            logger.debug("image.get_imgur_url=" + image.get_imgur_url())
                            u = urllib2.urlopen(image.get_imgur_url())
                        else:
                            logger.debug("image.local_path=" + image.local_path)
                            u = open(image.local_path, 'rb')
                        localpath = os.path.join(rootpath, image.filename)
                        logger.debug("localpath=" + localpath)
                        localFile = open(localpath, 'wb')
                        localFile.write(u.read())
                        localFile.close()
                        zipfile.write(localpath, os.path.join(dirname, image.filename))
                        os.remove(localpath)
                    except Exception, ex:
                        logger.error("%s of %s - image '%s' for email '%s' has failed : %s" % (j, totalimages, image.filename, job.email, str(ex)))
                zipfile.close()
                os.rmdir(rootpath)
                send_mail_download(zipname, job.galerie, job.email)
                job.is_intreatment = False
                job.is_treated = True
                job.path_to_zip = zipfilename
                job.save()
                logger.info("%s of %s - Job for email '%s' done !" % (i, nbtotal, job.email))
            except Exception, ex:
                logger.error("%s of %s - Job for email '%s' has failed : %s" % (i, nbtotal, job.email, str(ex)))
                job.is_intreatment = False
                job.is_treated = False
                job.save()
        logger.info("###### Zip for download creation done. ######")

        logger.info("###### Flag deprecated jobs as deleted ######")
        job_to_treat = DownloadJob.objects.filter(is_treated=True, is_deleted=False)
        for job in job_to_treat:
            if not os.path.exists(job.path_to_zip):
                job.is_deleted = True
                job.save()
        logger.info("###### Flag deprecated jobs as deleted done. ######")

def send_mail_download(zipname, galerie, email):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    downloadurl = "http://%s%s%s" % (domain, settings.TODOWNLOAD_URL, zipname)

    subject = "[CAL - Download] %s" % (galerie.titre)
    from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"

    text = render_to_string("galerie/mail_dl_galerie.html", {'galerie': galerie, 'downloadurl': downloadurl,})
    internal_sendmail(email, from_email, text, subject)
