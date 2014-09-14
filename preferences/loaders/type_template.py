"""
Wrapper for loading templates from site type directories. This mainly adds the path to any
existing TEMPLATE_DIRS and test is they exist.
"""

import os

from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from djblets.siteconfig.models import SiteConfiguration

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self):
        """
        Returns all matching template_dirs appended with the current site type path
        """
        siteconfig = SiteConfiguration.objects.get_current()
        current_site_type_path = siteconfig.get('site_config_path')
        for a_dir in settings.TEMPLATE_DIRS:
            new_dir = safe_join(a_dir, current_site_type_path)
            if os.path.exists(new_dir):
                yield new_dir

    def load_template_source(self, template_name, template_dirs=None):
        for filepath in self.get_template_sources():
            try:
                a_file = open(safe_join(filepath, template_name))
                try:
                    return (a_file.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    a_file.close()
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)

_loader = Loader()

def load_template_source(template_name, template_dirs=None):
    # For backwards compatibility
    import warnings
    warnings.warn(
        "'django.template.loaders.app_directories.load_template_source' is deprecated; use 'django.template.loaders.app_directories.Loader' instead.",
        DeprecationWarning
    )
    return _loader.load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
