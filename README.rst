.. image:: https://travis-ci.org/Atterratio/cmsplugin-slick.svg?branch=master
    :target: https://travis-ci.org/Atterratio/cmsplugin-slick
.. image:: https://codecov.io/gh/Atterratio/cmsplugin-slick/coverage.svg?branch=master
    :target: https://codecov.io/gh/Atterratio/cmsplugin-slick

===============
cmsplugin-slick
===============

Slick_ carousel plugin fo Django-CMS

.. _Slick: http://kenwheeler.github.io/slick/

.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://www.paypal.me/Atterratio
.. image:: https://img.shields.io/badge/Donate-YaMoney-orange.svg
   :target: https://money.yandex.ru/to/410011005689134

REQUIREMENTS
============

* *Python >= 3.3*
* *Django >= 1.8*
* *Django-CMS >=3.3*

INSTALLATION
============

* run :code:`pip install cmsplugin-slick` or :code:`pip install git+https://github.com/Atterratio/cmsplugin-slick.git`;
* add :code:`cmsplugin_slick` to your :code:`INSTALLED_APPS`;
* run :code:`manage.py migrate`;

UPDATE
======
Migrate to version 0.3.0 and older, from versions lesser 0.3.0 don't support. Remove all older version and install this.

Components and Usage
====================
Module :code:`Slick Carousel` contains the following plugins :code:`Slick Carousel`, 
:code:`Wrapped Slide`, :code:`CarouselFolderImages`

Slick Carousel
--------------
Parent slider plugin. Any other plugin can be added as a child (as a slide), 
or you can use special plugins, that generate a list of elements 
(see :code:`SlickCarouselFolderImagePlugin` for one such example)

Wrapped Slide
-------------
Allow wrapp several Django-CMS plugins like one slide. For example you can add :code:`image` and :code:`text` plugis, and text will be like caption for image.

Image Folder Carousel
---------------------
Returns images from :code:`filer` folder as carousel slides

Notes
=====
By default plugin used oficial slick CDN :code:`//cdn.jsdelivr.net/jquery.slick/1.6.0/`,
if you want update version, you can put in :code:`static/cmsplugin_slick/slick`
folder of you project prefered slick project files, or add :code:`SLICK_CDN` setting
in you progect :code:`settigs.py` file. Local files have a higher priority.