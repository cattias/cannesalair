from django.conf import settings, global_settings
from django.core.exceptions import ImproperlyConfigured
from djblets.log import siteconfig as log_siteconfig
from djblets.siteconfig.django_settings import apply_django_settings, \
                                               get_django_defaults, \
                                               get_django_settings_map
from djblets.siteconfig.models import SiteConfiguration

"""
missing settings
DEBUG
TEMPLATE_DEBUG
ADMINS
MANAGERS
DATABASES
SQLITE_DATABASES
SITE_ID
USE_I18N
SITE_ROOT
LOGIN_URL
LOGOUT_URL
LOGIN_REDIRECT_URL
LOCAL_ROOT
TOUPLOAD_ROOT
TODOWNLOAD_ROOT
TODOWNLOAD_URL
ADMIN_MEDIA_PREFIX
SECRET_KEY
TEMPLATE_LOADERS
TEMPLATE_CONTEXT_PROCESSORS
MIDDLEWARE_CLASSES
CAL_ROOT
SITE_ROOT_URLCONF
ROOT_URLCONF
INSTALLED_APPS
MEDIA_SERIAL_DIRS
AUTHENTICATION_BACKENDS
"""

# A mapping of siteconfig setting names to Django settings.py names.
# This also contains all the djblets-provided mappings as well.
settings_map = {
    'conf_webmaster_mail':                  'WEBMASTER_MAIL',
    'nav_page_count_size':                  'PAGE_COUNT_SIZE',
    'nav_max_size':                         'NAV_MAX_SIZE',
    'connected_after_last_req':             'CONNECTED_AFTER_LAST_REQ',
    'auth_profile_module':                  'AUTH_PROFILE_MODULE',
    'google_calendar_email':                'CALENDAR_EMAIL',
    'google_calendar_password':             'CALENDAR_PASSWORD',
    'google_analytics_account':             'ANALYTICS_ACCOUNT',
    'google_analytics_domain':              'ANALYTICS_DOMAIN',
    'imgur_auth_anon_key':                  'ANON_KEY',
    'imgur_auth_consumer_key':              'CONSUMER_KEY',
    'imgur_auth_consumer_secret':           'CONSUMER_SECRET',
    'imgur_password':                       'IMGUR_PASSWORD',
    'imgur_account':                        'IMGUR_ACCOUNT',
    'imgur_signin_url':                     'IMGUR_SIGNIN_URL',
    'imgur_api_endpoint':                   'IMGUR_API_ENDPOINT',
    'imgur_api_version':                    'IMGUR_API_VERSION',
    'imgur_api_account':                    'IMGUR_API_ACCOUNT',
    'imgur_api_format':                     'IMGUR_API_FORMAT',
    'site_config_path':                     'SITE_CONFIG_PATH',
    'site_activite_en_premier':             'SITE_ACTIVITE_EN_PREMIER',
    'site_background_image':                'SITE_BACKGROUND_IMAGE',
    'site_id':                              'SITE_ID',
}
settings_map.update(get_django_settings_map())
settings_map.update(log_siteconfig.settings_map)


# All the default values for settings.
defaults = get_django_defaults()
defaults.update(log_siteconfig.defaults)
defaults.update({
    'conf_webmaster_mail':                  '',
    'nav_page_count_size':                  50,
    'nav_max_size':                         6,
    'connected_after_last_req':             60,
    'auth_profile_module':                  'account.Profil',
    'google_calendar_email':                '',
    'google_calendar_password':             '',
    'google_analytics_account':             '',
    'google_analytics_domain':              '',
    'imgur_auth_anon_key':                  '',
    'imgur_auth_consumer_key':              '',
    'imgur_auth_consumer_secret':           '',
    'imgur_password':                       '',
    'imgur_account':                        '',
    'imgur_signin_url':                     '',
    'imgur_api_endpoint':                   '',
    'imgur_api_version':                    '',
    'imgur_api_account':                    '',
    'imgur_api_format':                     '',
    'site_config_path':                     'default',
    'site_activite_en_premier':             False,
    'site_background_image':                '/media/images/background.jpg',
    'site_id':                              2,

    # Overwrite this.
    'site_media_url': settings.SITE_ROOT + "media/"
})


def load_site_config():
    """
    Loads any stored site configuration settings and populates the Django
    settings object with any that need to be there.
    """
    def apply_setting(settings_key, db_key, default=None):
        db_value = siteconfig.settings.get(db_key)

        if db_value:
            setattr(settings, settings_key, db_value)
        elif default:
            setattr(settings, settings_key, default)


    try:
        siteconfig = SiteConfiguration.objects.get_current()
    except SiteConfiguration.DoesNotExist:
        raise ImproperlyConfigured, \
            "The site configuration entry does not exist in the database. " \
            "Re-run `./manage.py` syncdb to fix this."
    except:
        # We got something else. Likely, this doesn't exist yet and we're
        # doing a syncdb or something, so silently ignore.
        return


    # Populate defaults if they weren't already set.
    if not siteconfig.get_defaults():
        siteconfig.add_defaults(defaults)

    # The default value for DEFAULT_EMAIL_FROM (webmaster@localhost)
    # is less than good, so use a better one if it's set to that or if
    # we haven't yet set this value in siteconfig.
    mail_default_from = \
        siteconfig.settings.get('mail_default_from',
                                global_settings.DEFAULT_FROM_EMAIL)

    if (not mail_default_from or
        mail_default_from == global_settings.DEFAULT_FROM_EMAIL):
        domain = siteconfig.site.domain.split(':')[0]
        siteconfig.set('mail_default_from', 'noreply@' + domain)


    # Populate the settings object with anything relevant from the siteconfig.
    apply_django_settings(siteconfig, settings_map)


    # Now for some more complicated stuff...

    # Site administrator settings
    apply_setting("ADMINS", None, (
        (siteconfig.get("site_admin_name", ""),
         siteconfig.get("site_admin_email", "")),
    ))

    apply_setting("MANAGERS", None, settings.ADMINS)

    # Explicitly base this off the MEDIA_URL
    apply_setting("ADMIN_MEDIA_PREFIX", None, settings.MEDIA_URL + "admin/")

