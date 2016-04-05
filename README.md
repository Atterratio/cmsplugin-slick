#cmsplugin-slick
-----
Django-CMS plugin for [slik carousel](http://kenwheeler.github.io/slick/).
##Install
```
pip install git+https://github.com/Atterratio/cmsplugin-slick.git
```
Then add `cmsplugin_slick` to `INSTALLED_APPS` an run `manage.py migrate`

##Components and Usage
Module `Slick Carousel` contains the following plugins `Carousel Plugin`, `Plugins Wrapper`, `Image Folder Carousel`

###Carousel Plugin
Allow add Django-CMS plugin like one slide, ore multislide if plugin return not wrapped list of ellements, see my plugin `Image Folder Carousel`

###Plugins Wrapper
Alolow wrapp several Django-CMS plugins like one slide. For example you can add to this plugin `text` and `image` plugis, and text will be like title for image.

###Image Folder Carousel
Returns images from `filer` folder as carousel slides
