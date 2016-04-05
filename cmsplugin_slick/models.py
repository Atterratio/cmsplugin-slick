from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from filer.fields.folder import FilerFolderField
from cmsplugin_filer_utils import FilerPluginManager

from django.db import models

# Create your models here.
class Carousel(CMSPlugin):
    """
    Store main settings for carousel
    """
    #None
    title = models.CharField(verbose_name=_('Title'), max_length=60, blank=True)
    
    infinite = models.BooleanField(verbose_name=_('Infinite'), default=True)
    
    speed = models.IntegerField(verbose_name=_('Speed'), default=300)
    
    dots = models.BooleanField(verbose_name=_('Dots'), default=True)
    arrows = models.BooleanField(verbose_name=_('Arrows'), default=True)
    
    slides_to_show = models.IntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.IntegerField(verbose_name=_('Slides to scroll'), default=1)
    
    #Autoplay
    autoplay = models.BooleanField(verbose_name=_('Autoplay'), default=False)
    autoplay_speed = models.IntegerField(verbose_name=_('Autoplay speed'), null=True, blank=True)
    
    pause_on_hover = models.BooleanField(verbose_name=_('Pause on hover'), default=True)
    pause_on_dots_hover = models.BooleanField(verbose_name=_('Pause on dots hover'), default=False)
    
        
    #Other
    fade = models.BooleanField(verbose_name=_('Fade animation'), default=False)
    
    center_mode = models.BooleanField(verbose_name=_('Center mode'), default=False)
    center_padding = models.CharField(verbose_name=_('Center padding'), max_length=10, blank=True)
    
    variable_width = models.BooleanField(verbose_name=_('Variable Width'), default=False)
    
    vertical = models.BooleanField(verbose_name=_('Vertical'), default=False)  
    rigth_to_left = models.BooleanField(verbose_name=_('Right to left'), default=False)
    
    
    #Advanced
    classes = models.TextField(verbose_name=_('Css classes'), blank=True)
    
    
    def copy_relations(self, oldinstance):
        self.breakpoints = oldinstance.breakpoints.all()
    
class CarouselBreakpoint(models.Model):
    """
    Carousel break point allow create sesponsive carousels
    """
    carousel = models.ForeignKey('Carousel', related_name='breakpoints', verbose_name=_('Carousel'))
    
    breakpoint = models.IntegerField(verbose_name=_('Breakpoint resolution'))  
    
    slides_to_show = models.IntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.IntegerField(verbose_name=_('Slides to scroll'), default=1)
    
    
class CarouselElementWrapper(CMSPlugin):    
    classes = models.TextField(verbose_name=_('Css classes'), blank=True)
    
class CaroselImageFolder(CMSPlugin):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    folder = FilerFolderField(null=True, on_delete=models.SET_NULL)
    
    #objects = FilerPluginManager(select_related=('folder',))
    
    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        if self.title:
            return self.title
        elif self.folder_id and self.folder.name:
            return self.folder.name
        return "<empty>"
    