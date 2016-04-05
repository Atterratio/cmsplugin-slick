import json
from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from filer.models.imagemodels import Image

from .models import Carousel, CarouselBreakpoint, CarouselElementWrapper, CaroselImageFolder

class CarouselBreakpointInline(admin.StackedInline):
    model = CarouselBreakpoint
    extra = 0

class CarouselPlugin(CMSPluginBase):
    """
    Main carousel plugin that parent for others plugin.
    Supossed one plugin - one slide, or support plugins that get list of ellements, see my filler folder galery
    """
    model = Carousel
    render_template = "cmsplugin_slick/carousel.djhtml"
    module = 'Slick Carousel'
    name = 'Carousel Plugin'
    allow_children = True
    inlines = [CarouselBreakpointInline,]
    
    fieldsets = (
        (None, {'fields': (
                'title',
                'infinite',
                'speed',
                ('dots', 'arrows'),
                ('slides_to_show', 'slides_to_scroll'),
        )}),
        
        ('Autoplay', {
            'classes': ('collapse',),
            'fields': (
                ('autoplay', 'autoplay_speed'),
                ('pause_on_hover', 'pause_on_dots_hover'),
        )}),
                 
        ('Others Settings', {
            'classes': ('collapse',),
            'fields':(
                'fade',
                ('center_mode', 'center_padding'),
                'variable_width',
                ('vertical', 'rigth_to_left'),
        )}),
        
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (
                'classes',
            ),
        }),
    )
    
    def render(self, context, instance, placeholder):
        context = super(CarouselPlugin, self).render(context, instance, placeholder)
        slick_dict = {'infinite': instance.infinite,
                            'speed': instance.speed,
                            'dots': instance.dots, 'arrows': instance.arrows,
                            'slidesToShow': instance.slides_to_show, 'slidesToScroll': instance.slides_to_scroll,
                            'autoplay': instance.autoplay, 'autoplaySpeed': instance.autoplay_speed,
                            'pauseOnHover': instance.pause_on_hover, 'pauseOnDotsHover': instance.pause_on_dots_hover,
                            'fade': instance.fade,
                            'centerMode': instance.center_mode, 'centerPadding': instance.center_padding,
                            'variableWidth': instance.variable_width,'vertical': instance.vertical,
                            'rtl': instance.rigth_to_left}
        
        if instance.breakpoints.all():
            responsive = []
            for breakpoint in instance.breakpoints.all():
                responsive.append({'breakpoint': breakpoint.breakpoint,
                                   'settings': {'slidesToShow': breakpoint.slides_to_show,
                                                'slidesToScroll': breakpoint.slides_to_scroll}
                                   })
                
            slick_dict.update({'responsive': responsive})
            
        slick_settings = json.dumps(slick_dict)
            
        context.update({'slick_settings': slick_settings})
                
        return context
    
class CarouselElementWrapperPlugin(CMSPluginBase):
    """
    Include all child plugin as one slide
    """
    model = CarouselElementWrapper
    render_template = "cmsplugin_slick/element_wrapper.djhtml"
    module = 'Slick Carousel'
    name = 'Plugins Wrapper'
    #require_parent = True
    parent_classes = ['CarouselPlugin']
    allow_children = True
    
class CarouselImageFolderPlugin(CMSPluginBase):
    model = CaroselImageFolder
    render_template = "cmsplugin_slick/folder_carousel.djhtml"
    module = 'Slick Carousel'
    name = 'Image Folder Carousel'
    #require_parent = True
    parent_classes = ['CarouselPlugin']
        
    def get_folder_images(self, folder, user):
        qs_files = folder.files.instance_of(Image)
        if user.is_staff:
            return qs_files
        else:
            return qs_files.filter(is_public=True)
        
    def render(self, context, instance, placeholder):
        context = super(CarouselImageFolderPlugin, self).render(context, instance, placeholder)
        user = context['request'].user

        if instance.folder_id:
            folder_images = self.get_folder_images(instance.folder, user)
        else:
            folder_images = Image.objects.none()

        context.update({'folder_images': sorted(folder_images)})
        
        return context
    
    
plugin_pool.register_plugin(CarouselPlugin)
plugin_pool.register_plugin(CarouselElementWrapperPlugin)
plugin_pool.register_plugin(CarouselImageFolderPlugin)