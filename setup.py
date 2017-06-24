from setuptools import setup, find_packages
from cmsplugin_slick import __version__

REQUIREMENTS = [
    'django-cms>=3.3.0',
    'django>=1.7.0',
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='cmsplugin-slick',
    version=__version__,
    url='https://github.com/Atterratio/cmsplugin-slick',
    license='MIT',
    author='Aeternus Atterratio',
    author_email='atterratio@gmail.com',
    description='Slick carousel plugin fo Django-CMS',
    long_description=open('README.rst').read(),
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    keywords='Django Django-CMS Slick Carousel',
    packages=find_packages(),
    include_package_data=True,
)