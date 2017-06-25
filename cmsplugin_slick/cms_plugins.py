import json
import os
from django.contrib import admin
from django.template.loader import select_template
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from filer.models.imagemodels import Image
from cmsplugin_filer_image.conf import settings

from .models import SlickCarousel, SlickCarouselWrappedSlide, SlickCarouselFolderImages

class SlickCarouselPlugin(CMSPluginBase):
    '''
    Parent slider plugin.

    Any other plugin can be added as a child (as a slide), or you can use
    special plugins that generate a list of elements (see
    CarouselImageFolderPlugin below for one such example
    '''
    model = SlickCarousel
    render_template = "cmsplugin_slick/carousel.djhtml"
    module = _('Slick Carousel')
    name = _('Slick Carousel')
    allow_children = True

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slick_preset',
                'breakpoints',
            )
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'classes',
            )
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(SlickCarouselPlugin, self).render(
            context, instance, placeholder)
        
        slick_dict = {'slide': ':not(template)'}
        if instance.slick_preset:
            slick_dict.update({
                'infinite': instance.slick_preset.infinite,
                'speed': instance.slick_preset.speed,
                'dots': instance.slick_preset.dots,
                'arrows': instance.slick_preset.arrows,
                'slidesToShow': instance.slick_preset.slides_to_show,
                'slidesToScroll': instance.slick_preset.slides_to_scroll,
                'autoplay': instance.slick_preset.autoplay,
                'autoplaySpeed': instance.slick_preset.autoplay_speed,
                'pauseOnHover': instance.slick_preset.pause_on_hover,
                'pauseOnDotsHover': instance.slick_preset.pause_on_dots_hover,
                'fade': instance.slick_preset.fade,
                'rows': instance.slick_preset.rows,
                'slidesPerRow': instance.slick_preset.slides_per_row,
                'centerMode': instance.slick_preset.center_mode,
                'centerPadding': instance.slick_preset.center_padding,
                'variableWidth': instance.slick_preset.variable_width,
                'adaptiveHeight': instance.slick_preset.adaptive_height,
                'vertical': instance.slick_preset.vertical,
                'rtl': instance.slick_preset.rigth_to_left,
                'respondTo': instance.slick_preset.respond_to,
                'mobileFirst': instance.slick_preset.mobile_first,
            })
        
        if instance.breakpoints:
            breakpoints, responsive = self._get_breakpoints(instance)
            slick_dict.update({'responsive': responsive})
        
        breakpoints = json.dumps(breakpoints)
        slick_settings = json.dumps(slick_dict)

        try:
            os.path.isfile(finders.find('cmsplugin_slick/slick/slick.min.js'))
            os.path.isfile(finders.find('cmsplugin_slick/slick/slick.css'))
            
            slick_static_path = os.path.dirname(static('cmsplugin_slick/slick/slick.min.js'))
        except:
            try:
                slick_static_path = settings.SLICK_CDN
            except:
                slick_static_path = '//cdn.jsdelivr.net/jquery.slick/1.6.0/'

        context.update({
            'slick_settings': slick_settings,
            'breakpoints': breakpoints,
            'slick_static_path': slick_static_path,
        })

        return context

    def _get_breakpoints(self, instance):
        breakpoints = {}
        responsive = []
        for breakpoint in instance.breakpoints.breakpoints.all():
            breakpoint_settings = {
                'slidesToShow': breakpoint.slides_to_show,
                'slidesToScroll': breakpoint.slides_to_scroll,
            }

            if breakpoint.dots is not None:
                breakpoint_settings.update({'dots': breakpoint.dots})
            if breakpoint.arrows is not None:
                breakpoint_settings.update({'arrows': breakpoint.arrows})
                
            if breakpoint.center_mode is not None:
                breakpoint_settings.update({'center_mode': breakpoint.center_mode})
            if breakpoint.center_padding:
                breakpoint_settings.update({'centerPadding': breakpoint.center_padding})
                
            if breakpoint.autoplay is not None:
                breakpoint_settings.update({'autoplay': breakpoint.autoplay})
            if breakpoint.autoplay_speed:
                breakpoint_settings.update({'autoplaySpeed': breakpoint.autoplay_speed})

            breakpoints.update({breakpoint.breakpoint: breakpoint.slides_to_show})
            responsive.append({
                'breakpoint': breakpoint.breakpoint,
                'settings': breakpoint_settings,
            })

        return breakpoints, responsive


class SlickCarouselWrappedSlidePlugin(CMSPluginBase):
    '''
    Allow wrapp several Django-CMS plugins like one slide. For example you can add "image" 
    and "text" plugins, and text will be like caption for image.
    '''
    model = SlickCarouselWrappedSlide
    render_template = "cmsplugin_slick/element_wrapper.djhtml"
    module = _('Slick Carousel')
    name = _('Wrapped Slide')
    parent_classes = ['SlickCarouselPlugin', ]
    allow_children = True

    fieldsets = (
        (None, {
            'fields': [
                'title',
                'caption',
            ]
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'classes',
            )
        }),
    )


class SlickCarouselFolderImagesPlugin(CMSPluginBase):
    '''
    Returns images from "filer" folder as carousel slides
    '''
    model = SlickCarouselFolderImages
    render_template = "cmsplugin_slick/folder_carousel.djhtml"
    module = _('Slick Carousel')
    name = _('Carousel Folder Images')
    parent_classes = ['SlickCarouselPlugin', ]

    fieldsets = (
        (None, {
            'fields': [
                'title',
                'folder',
                'caption',
            ]
        }),
        (_('Image thumbnail options'), {
            'fields': (
                ('autoscale','thumbnail'),
                'thumbnail_option',
            )
        }),
        (_('Link options'), {
            'fields': (
                ('original_link', 'target_blank'),
            )
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                ('ordered_by', 'reverse_order'),
                'classes',
            )
        }),
    )

    def _get_thumbnail_options(self, context, instance):
        """
        Return the size and options of the thumbnail that should be inserted
        """
        width, height = 800, 800
        crop, upscale = True, True
        if instance.thumbnail_option:
            if instance.thumbnail_option.width:
                width = instance.thumbnail_option.width
            if instance.thumbnail_option.height:
                height = instance.thumbnail_option.height

            crop = instance.thumbnail_option.crop
            upscale = instance.thumbnail_option.upscale

        if crop:
            crop = "smart"

        return {
            'size': (width, height),
            'crop': crop,
            'upscale': upscale,
        }

    def get_thumbnail(self, context, instance):
        if instance.image:
            return instance.image.file.get_thumbnail(self._get_thumbnail_options(context, instance))

    def render(self, context, instance, placeholder):
        context = super(SlickCarouselFolderImagesPlugin, self).render(context, instance, placeholder)
        user = context['request'].user
        folder_images = instance.folder.files.instance_of(Image)
        if user.is_staff:
            pass
        elif user.id is None: 
            folder_images = instance.folder.files.filter(is_public=True)
        else:
            folder_images = instance.folder.files.filter(Q(is_public=True) | Q(owner=user))

        if instance.reverse_order:
            folder_images = folder_images.order_by('-{}'.format(instance.ordered_by))
        else:
            folder_images = folder_images.order_by(instance.ordered_by)

        options = self._get_thumbnail_options(context, instance)
        context.update({
            'folder_images': folder_images,
            'instance': instance,
            'opts': options,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(SlickCarouselPlugin)
plugin_pool.register_plugin(SlickCarouselWrappedSlidePlugin)
plugin_pool.register_plugin(SlickCarouselFolderImagesPlugin)