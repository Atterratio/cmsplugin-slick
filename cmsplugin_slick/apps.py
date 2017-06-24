from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SlickConfig(AppConfig):
    name = 'cmsplugin_slick'
    verbose_name = _('Django-CMS plugin for Slick carousel')