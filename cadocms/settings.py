import socket, sys, pkgutil, os
from configurations import Settings as BaseSettings

class Settings(BaseSettings):
    
    CADO_NAME = 'Cado CMS'
    SECRET_KEY = 'OVERWRITE ME'
    
    SITE_ID = 1
    MULTISITE = False
    
    @property
    def PROJECT_ROOT(self):
        package = pkgutil.get_loader(self.__class__.__module__)
        return os.path.dirname(os.path.dirname(package.filename))

    @property
    def CONFIG_GEN_GENERATED_DIR(self):
        return os.path.join(self.PROJECT_ROOT, 'config')

    @property
    def CONFIG_GEN_TEMPLATES_DIR(self):
        return os.path.join(self.PROJECT_ROOT, 'config_templates')

    ADMINS = (
              ('Franciszek Szczepan Wawrzak', 'frank.wawrzak@cadosolutions.com'),
    )

    MANAGERS = ADMINS
    
    @property
    def DATABASES(self):
        #print 'XXXX'
        databases = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
        
        databases['default'].update(self.HOST.DATABASE)
                               
        if 'test' in sys.argv:
            databases['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
        #print databases
        return databases
    
    
    CADO_DOMAIN = 'localhost' 
    
    @property
    def CADO_FULL_DOMAIN(self):
        if (self.HOST.CLASS == 'DEV'):
            return 'localhost:8000'
        elif (self.HOST.CLASS == 'TEST'):
            return self.HOST.CLASS.lower() + '.' + self.CADO_DOMAIN
        else:
            return self.CADO_DOMAIN
    
    @property
    def CADO_PROJECT_GROUP(self):
        return self.CADO_PROJECT
     
    CADO_FLAVOURS = [
        ('desktop', 'Desktop Version', ''),
        ('simple', 'Simplified Version', 's.'),
        ('mobile', 'Mobile Version', 'm.'),
        ('touch', 'Smartphone Version', 'i.'),
        ('accessible', 'Accessible Version', 'ac.'),
    ]
    
    @property
    def DEBUG(self):
        return (self.HOST.CLASS == 'DEV') or (self.HOST.CLASS == 'TEST') 
        
    @property
    def TEMPLATE_DEBUG(self):
        return self.DEBUG
    
    @property
    def EMAIL_BACKEND(self):
        if (self.HOST.CLASS == 'DEV'):
            return 'django.core.mail.backends.console.EmailBackend'
        return super(Settings, self).EMAIL_BACKEND
    
    TIME_ZONE = 'America/Chicago'
    
    LANGUAGE_CODE = 'en'
    
    LANGUAGES = (
        ('en', 'English'),
    )
    
    CADO_DEFAULT_LANGUAGE = 'en'
    CADO_LANGUAGES = ('en')
    
    USE_I18N = True
    USE_L10N = True
    
    USE_TZ = True
    
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    ADMIN_URL = '/admin/'
    
    
    @property
    def MEDIA_ROOT(self):
        if self.MULTISITE:
            return self.HOST.APPROOT + 'media/' + self.CADO_PROJECT + '/'
        else:
            return self.HOST.APPROOT + 'media/'
    
    @property
    def STATIC_ROOT(self):
        if self.MULTISITE:
            return self.HOST.APPROOT + 'static/' + self.CADO_PROJECT + '/'
        else:
            return self.HOST.APPROOT + 'static/'

    @property   
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return ("django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.request",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.core.context_processors.tz",
            "django.contrib.messages.context_processors.messages")

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )
    
    TEMPLATE_LOADERS = (
        'cadocms.loaders.flavour.Loader',
        'hamlpy.template.loaders.HamlPyFilesystemLoader',
        'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',  
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'cadocms.middleware.Middleware',
        #'versioning.middleware.VersioningMiddleware',
    )
    
    @property
    def ROOT_URLCONF(self):
        return self.CADO_PROJECT +'.urls'
    
    @property
    def WSGI_APPLICATION(self):
        return 'cadocms.wsgi.application'
    
    @property
    def INSTALLED_APPS(self):
        #print 'INSTALLED_APPS cadocms'
        return (
            'cadocms.db_prefix',
            self.CADO_PROJECT,
            'cadocms',
            'grappelli.dashboard',
            'grappelli',
            'filebrowser',
        ) + super(Settings, self).INSTALLED_APPS + (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django_config_gen',
            'reversion',
            'haystack',
            'south',
            'compressor',
            'mptt',
            'debug_toolbar',
            #'versioning',
            'captcha',
            'geoposition',
            'imagekit',
            'rosetta',
            'modeltranslation',
        )
    CAPTCHA_FONT_SIZE = 25
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
    CAPTCHA_FILTER_FUNCTIONS = ('captcha.helpers.post_smooth',)
    CAPTCHA_LETTER_ROTATION = (-10,10)
    CAPTCHA_LENGTH = 6
    
    GRAPPELLI_INDEX_DASHBOARD = 'cadocms.dashboard.CustomIndexDashboard'

    INTERNAL_IPS = ('127.0.0.1',)
    
    
    @property
    def HAYSTACK_CONNECTIONS(self):
        if self.HOST.SOLR_PATH:
            return {
                'default': {
                            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
                            'URL': self.HOST.SOLR_PATH + self.CADO_PROJECT + '/',
                            },
                }
        else:
            return {
                'default': {
                            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
                    },
                }
        
    
    @property
    def GRAPPELLI_ADMIN_TITLE(self):
        return self.CADO_NAME + ' Admin'
    
    
    SOLR_PATH = '/opt/solr/unravelling/'
    
    COMPRESS_PRECOMPILERS = (
        ('text/coffeescript', 'coffee --compile --stdio'),
        #('text/less', 'lessc {infile} {outfile}'),
        #('text/x-sass', 'sass {infile} {outfile}'),
        #('text/x-scss', 'sass --scss {infile} {outfile}'),
        #('text/stylus', 'stylus < {infile} > {outfile}'),
        ('text/x-scss', 'cadocms.filters.SassFilter'),
    )

    COMPRESS_PARSER = 'compressor.parser.HtmlParser' 
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS' : False
    } 
    """
    TINYMCE_DEFAULT_CONFIG = {
            'plugins': "table,paste,searchreplace,preview",
            'theme': "advanced",
            'cleanup_on_startup': True,
            'custom_undo_redo_levels': 10,
            'theme_advanced_resizing': True,
            'content_css': STATIC_URL + 'content.css',
            'body_class': 'content',
            'height': 400,
    }
    """

    @property
    def HOST(self):
        if not hasattr(self, '_HOST'):
            host_name = socket.gethostname()
            host_srcroot = os.getcwd()
            #package = pkgutil.get_loader(self.__class__.__module__)
            #srcroot = os.path.dirname(os.path.dirname(package.filename))
            CurrentHostSettingsClass = DevHostSettings
            found = False
            for HostSettingsClass in HostSettings.__subclasses__():
                if HostSettingsClass.NAME == host_name and HostSettingsClass.SRCROOT == host_srcroot:
                    CurrentHostSettingsClass = HostSettingsClass
                    found = True
            #if not found:
                #print 'THIS SEEMS LIKE A DEV SERVER'
            self._HOST = CurrentHostSettingsClass
            
        return self._HOST

class MultiAppSettings(Settings):
    
    MULTISITE = True
    @property
    def SITES(self):
        if not hasattr(self, '_SITES'):
            sites = []
            if os.environ.get("CADO_SITES", "").split(";"):
                for name in os.listdir(os.getcwd()):
                    if os.path.isdir(os.path.join(os.getcwd(), name)):
                        if os.path.isfile(os.path.join(os.getcwd(), name, 'settings.py')):
                            if not name + '.settings' == os.environ["DJANGO_SETTINGS_MODULE"]:
                                sites.append(name)
                self._SITES = []
                for site in sites:
                    _temp = __import__(site + '.settings', globals(), locals(), ['Settings'], -1) 
                    self._SITES.append(_temp.Settings())
            else:
                self._SITES = [self]
                
        return self._SITES
    
    """
    @property
    def DB_PREFIX(self):
        return self.CADO_PROJECT + '_'
    """

class HostSettings(object):
    PYTHON_PREFIX = "~/virtualenv/bin/"
    SOLR_PATH = 'http://127.0.0.1:8080/solr/'

class DevHostSettings(HostSettings):
    SOLR_PATH = None
    CLASS = 'DEV'
    NAME = 'localhost'
    SRCROOT = os.getcwd() + '/'
    APPROOT = os.getcwd() + '/'
    DATABASE = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME' : 'local.db3'
                }
