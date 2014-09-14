from django import template
from django.conf import settings
from djblets.siteconfig.models import SiteConfiguration
from ConfigParser import ConfigParser
import os
import logging

register = template.Library()

_RESOURCES_CACHE = {}

current_preferences = ()

@register.simple_tag
def tp(section, name, *args, **kwargs):
    """
    Renders a preference from a given template
    """
    
    def get_current_preferences():
        """
        cache the default resources to speed up the process
        """
        global _RESOURCES_CACHE
        siteconfig = SiteConfiguration.objects.get_current()
        if siteconfig.id not in _RESOURCES_CACHE or os.path.getmtime(_RESOURCES_CACHE[siteconfig.id][1]) > _RESOURCES_CACHE[siteconfig.id][2]:
            if siteconfig.id not in _RESOURCES_CACHE:
                resources_path = os.path.join(settings.MAIN_TEMPLATE_DIRS,siteconfig.get('site_config_path'),'resources.properties')
            else:
                resources_path = _RESOURCES_CACHE[siteconfig.id][1]
            cfg = ConfigParser()
            if os.path.exists(resources_path):
                logger = logging.getLogger('preferences')
                logger.info("reading preferences from %s" % resources_path)
                cfg.read(resources_path)
            _RESOURCES_CACHE[siteconfig.id] = (cfg, resources_path, os.path.getmtime(resources_path), )

        return _RESOURCES_CACHE[siteconfig.id][0]

    result = None
    if get_current_preferences().has_option(section, name):
        result = get_current_preferences().get(section, name)
    
    # print "[%s]%s=%s" % (section, name, result)
    return result
