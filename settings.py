# Django settings for cannesalair project.
import os
from ConfigParser import ConfigParser

cfg = ConfigParser()
cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.properties"))

DEBUG = cfg.get("debug", "DEBUG") == "True"
TEMPLATE_DEBUG = cfg.get("debug", "TEMPLATE_DEBUG") == "True"

ADMINS = (
    (cfg.get("admin", "ADMIN_NAME"), cfg.get("admin", "ADMIN_MAIL")),
)
WEBMASTER_MAIL = cfg.get("webmaster", "WEBMASTER_MAIL")
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': cfg.get("database", "DATABASE_NAME"),
        'ENGINE': 'django.db.backends.mysql',
        'USER': cfg.get("database", "DATABASE_USER"),
        'PASSWORD': cfg.get("database", "DATABASE_PASSWORD"),
        'HOST': cfg.get("database", "DATABASE_HOST"),
        'PORT': cfg.get("database", "DATABASE_PORT"),
        'OPTIONS': {"init_command": "SET storage_engine=INNODB",},
    },
}

SQLITE_DATABASES = {
    'default': {
        'NAME': 'c:\\dev\\database.sl3',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

SITE_ID = cfg.get("site", "SITE_ID")

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
SITE_ROOT = '/'
LOGIN_URL = SITE_ROOT + 'account/login/'
LOGOUT_URL = SITE_ROOT + 'account/logout/'
LOGIN_REDIRECT_URL = '/article/'

LOCAL_ROOT = os.path.dirname(__file__)
SECURE_ROOT = os.path.join(LOCAL_ROOT, 'secure')
MEDIA_ROOT = os.path.join(LOCAL_ROOT, 'media')

FILES_ROOT = os.path.join(MEDIA_ROOT, 'files')
if not os.path.exists(FILES_ROOT):
    os.makedirs(FILES_ROOT)

TOUPLOAD_ROOT = os.path.join(FILES_ROOT, 'toupload')
if not os.path.exists(TOUPLOAD_ROOT):
    os.makedirs(TOUPLOAD_ROOT)

TODOWNLOAD_ROOT = os.path.join(FILES_ROOT, 'todownload')
if not os.path.exists(TODOWNLOAD_ROOT):
    os.makedirs(TODOWNLOAD_ROOT)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = SITE_ROOT + 'media/'
FILES_URL = MEDIA_URL + 'files/'
TOUPLOAD_URL = FILES_URL + 'toupload/'
TODOWNLOAD_URL = FILES_URL + 'todownload/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'b_vkd2nk9k8yfrkj31qtfga^wu_)k0_hyxu81vn#q-us=fy=$h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'preferences.loaders.type_template.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'djblets.siteconfig.context_processors.siteconfig',
    'djblets.util.context_processors.settingsVars',
    'djblets.util.context_processors.siteRoot',
    'djblets.util.context_processors.ajaxSerial',
    'djblets.util.context_processors.mediaSerial',
    'core.context_processors.activetab',
    'core.context_processors.next_page',
    'article.context_processors.latestarticles',
    'sortie.context_processors.sortiesavenir',
    'forum.context_processors.latestmessages',
    'log.context_processors.notifications',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', # Keep this first.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # These must go before anything that deals with settings.
    'djblets.siteconfig.middleware.SettingsMiddleware',
    'djblets.log.middleware.LoggingMiddleware',
    'core.middleware.threadlocals.ThreadLocals', 
)

CAL_ROOT = os.path.abspath(os.path.split(__file__)[0])
SITE_ROOT_URLCONF = 'urls'
ROOT_URLCONF = 'djblets.util.rooturl'

MAIN_TEMPLATE_DIRS = os.path.join(CAL_ROOT, 'templates')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    MAIN_TEMPLATE_DIRS,
    '/home/cattias/install/lib/python2.6/site-packages/debug_toolbar/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sites',
    'django.contrib.sessions',
    'djblets.siteconfig',
    'djblets.util',
    # Internal applications
    'admin',
    'core',
    'log',
    'comment',
    'article',
    'forum',
    'sortie',
    'galerie',
    'account',
    'matos',
    'meteo',
    # External applications
    'photologue',
    'tagging',
    'captcha',
    'django.contrib.databrowse',
    'djangogcal',
    'preferences',
    'south',
)

MEDIA_SERIAL_DIRS = (
    'css',
    'images',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

PAGE_COUNT_SIZE = 50 
NAV_MAX_SIZE = 6 

# seconds
CONNECTED_AFTER_LAST_REQ = 60
AUTH_PROFILE_MODULE = 'account.Profil'

EMAIL_HOST = cfg.get("email", "EMAIL_HOST")
EMAIL_PORT = int(cfg.get("email", "EMAIL_PORT"))
EMAIL_HOST_USER = cfg.get("email", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = cfg.get("email", "EMAIL_HOST_PASSWORD")

# Google settings
CALENDAR_EMAIL=cfg.get("google", "CALENDAR_EMAIL")
CALENDAR_PASSWORD=cfg.get("google", "CALENDAR_PASSWORD")
ANALYTICS_ACCOUNT=cfg.get("google", "ANALYTICS_ACCOUNT")

# Imgur settings
ANON_KEY=cfg.get("imgur", "ANON_KEY")
CONSUMER_KEY=cfg.get("imgur", "CONSUMER_KEY")
CONSUMER_SECRET=cfg.get("imgur", "CONSUMER_SECRET")
IMGUR_PASSWORD=cfg.get("imgur", "PASSWORD")
IMGUR_ACCOUNT=cfg.get("imgur", "ACCOUNT")
IMGUR_SIGNIN_URL = "http://api.imgur.com/2/signin"

IMGUR_API_ENDPOINT="http://api.imgur.com"
IMGUR_API_VERSION="2"
IMGUR_API_ACCOUNT="account"
IMGUR_API_FORMAT="json"

#Site settings
SITE_BACKGROUND_IMAGE=cfg.get("site", "BACKGROUND_IMAGE")

