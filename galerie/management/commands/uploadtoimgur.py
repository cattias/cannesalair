from django.core.management.base import BaseCommand
import sys
from galerie.models import Photo, Galerie
from galerie import upload_image_to_imgur_album, link_image_to_imgur_album,\
    create_album
import logging

class Command(BaseCommand):

    help = 'Upload local images to imgur'
    stdout = sys.stdout
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """Does the job."""
        # create logger with 'uploader'
        logger = logging.getLogger('uploader')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('upload.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        # logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("###### Starting album creation ######")
        i=0
        album_to_treat = Galerie.objects.filter(is_created=False, is_intreatment=False)
        nbtotal = album_to_treat.count()
        for g in album_to_treat:
            g.intreatment = True
            g.save()
        for galerie in album_to_treat:
            i+=1
            logger.info("%s of %s - Creating album for galerie '%s'" % (i, nbtotal, galerie.titre))
            imgur_id = create_album(galerie.titre_slug)
            if imgur_id:
                galerie.imgur_id = imgur_id
                galerie.is_created = True
                galerie.is_intreatment = False
                galerie.save()
                logger.info("%s - Creation Successful" % galerie.titre_slug)
            else:
                galerie.is_intreatment = False
                galerie.save()
                logger.error("%s - Creation Fail" % galerie.titre_slug)
        logger.info("###### Album creation done. ######")
        
        logger.info("###### Starting upload ######")
        i=0
        photos_to_treat = Photo.objects.filter(is_uploaded=False, is_intreatment=False, galerie__is_created=True)
        nbtotal = photos_to_treat.count()
        for p in photos_to_treat:
            p.intreatment = True
            p.save()
        for image in photos_to_treat:
            i+=1
            logger.info("%s of %s - Uploading image '%s' in album %s" % (i, nbtotal, image.filename, image.galerie.imgur_id))
            if upload_image_to_imgur_album(image):
                logger.info("%s - Upload Successful" % image.filename)
            else:
                logger.error("%s - Upload Fail" % image.filename)
        logger.info("###### Upload done. ######")

        logger.info("###### Starting link ######")
        i=0
        photos_to_treat = Photo.objects.filter(is_uploaded=True, is_linked=False, is_intreatment=False, galerie__is_created=True)
        nbtotal = photos_to_treat.count()
        for p in photos_to_treat:
            p.intreatment = True
            p.save()
        for image in photos_to_treat:
            i+=1
            logger.info("%s of %s - Linking image '%s' to album %s" % (i, nbtotal, image.hash, image.galerie.imgur_id))
            if link_image_to_imgur_album(image):
                logger.info("%s - Link Successful" % image.hash)
            else:
                logger.error("%s - Link Fail" % image.hash)
        logger.info("###### Link done. ######")
