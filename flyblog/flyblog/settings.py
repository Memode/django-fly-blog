# coding:utf-8
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd3zl36_sdsk=+w9#4v!m5=49szl3+dtogv*!pxc3%o9o^+q8w_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '.sinaapp.com']

# 一些公共的参数

PAGE_NUM = 10
RECENTLY_NUM = 6
HOT_NUM = 6
ONE_DAY = 24 * 60 * 60
FIF_MIN = 15 * 60
FIVE_MIN = 5 * 60

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'pagedown',
    'markdown_deux',
    'tinymce',
    'ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
ROOT_URLCONF = 'flyblog.urls'

WSGI_APPLICATION = 'flyblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
SAE = False
if not SAE:
    DOMAIN = 'http://localhost:8000'
    DATABASES = {
        # 'default2': {
        #    'ENGINE': 'django.db.backends.sqlite3',
        #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'flyblog',
            'USER': 'root',
            'PASSWORD': '199288',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
else:
    DOMAIN = 'http://pyfor.sinaapp.com'
    import sae.const
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': sae.const.MYSQL_DB,
            'USER': sae.const.MYSQL_USER,
            'PASSWORD': sae.const.MYSQL_PASS,
            'HOST': sae.const.MYSQL_HOST,
            'PORT': sae.const.MYSQL_PORT,

        }
    }
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
# 模板调用路径
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    #os.path.join(os.path.dirname(__file__), 'blog/templates'),
)

# Django-suit后台配置公共参数
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'flyblog',
}

# tinymce config
'''
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "bbcode,emotions,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'theme_advanced_buttons3_add': "emotions,code",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_styles': "Code=codeStyle;Quote=quoteStyle",
    'content_css': "bbcode.css",
    'entity_encoding': "raw",
    'add_unload_trigger': False,
    'remove_linebreaks': False
}
'''
# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
'''
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 500,
        'width': 600,
    },
}
'''
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-', 'Preview'],
            ['Undo', 'Redo', 'RemoveFormat'],
            ['Bold', 'Italic', 'Underline', 'Strike',
                '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-',
                'Outdent', 'Indent', 'Blockquote'],
            ['Link', 'Unlink', 'Anchor', 'Image', 'HorizontalRule',
                'Smiley', 'Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             'pbckcode', 'About'],
        ),
        'height': 500,
        'width': 600,
        'allowedContent': True
    }
}
