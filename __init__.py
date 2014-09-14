# The version of Review Board.
#
# This is in the format of:
#
#   (Major, Minor, Micro, Patch, alpha/beta/rc/final, Release Number, Released)
#

from admin import get_version_string, get_package_version, VERSION

def initialize():
    """Begins initialization of Review Board.

    This sets up the logging, generates cache serial numbers, and then
    fires an initializing signal that other parts of the codebase can
    connect to. This must be called for such features as e-mail notification
    to work.
    """
    import logging
    import os

    from django.conf import settings
    from djblets.util.misc import generate_cache_serials
    from djblets import log

    # Set up logging.
    log.init_logging()
    if settings.DEBUG:
        logging.debug("Log file for Review Board v%s (PID %s)" %
                      (get_version_string(), os.getpid()))

    # Generate cache serials
    generate_cache_serials()

__version_info__ = VERSION[:-1]
__version__ = get_package_version()
