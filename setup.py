# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='django-cadolib',
    version='0.1.0',
    description='Simple set of tiny usefull bits',
    author='Frank Wawrzak (CadoSolutions)',
    author_email='frank.wawrzak@cadosolutions.com',
    url='https://github.com/fsw/django-cadolib',
    download_url='git://github.com/fsw/django-cadolib.git',
    packages=['cadolib'],
    install_requires=[
        'PIL==1.1.7',
        'django-compressor==1.2',
        'django-imagekit==2.0.3',
        'django-mptt==0.5.5',
        'pilkit==0.1.3',
        'pysolr==3.0.3',
        'simplejson==2.3.2',
        'six==1.2.0',
        'python-dateutil==2.1',
        'flup',
        'pdfdocument==1.4',
        'reportlab==2.5',
        'openpyxl==1.6.1',
        'lxml==3.0',
        'django-debug-toolbar==0.9.4',
        'django-versioning==0.7.3',
        'hamlpy==0.82.2',
        'html2text',
        'Pillow >=2.0.0',
        'django-tinymce',
        'django-filebrowser',
        'django-geoposition',
    ],
)