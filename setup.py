# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path


# with open('README.rst') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [
    'Django>=1.9',
    'django-cms>=3',
    'django-filer'
]


setup(
    name='cmsplugin-slick',
    version='0.2.3',
    description='Django-CMS plugin for slick carousel',
    long_description='',
    author='Alexander Paramonov',
    author_email='alex@paramono.com',
    # long_description=readme + '\n\n' + history,
    url='https://github.com/paramono/cmsplugin-slick',
    packages=[
        'cmsplugin_slick'
    ],
    package_dir={'cmsplugin_slick':
                 'cmsplugin_slick'},
    include_package_data=True,
    install_requires=requirements,
    keywords='Django CMS slick slider plugin',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='GPLv3+',
)
