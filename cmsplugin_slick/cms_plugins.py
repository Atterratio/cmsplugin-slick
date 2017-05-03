import json
from django.contrib import admin
from django.template.loader import select_template
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from filer.models.imagemodels import Image
from cmsplugin_filer_image.conf import settings

from .models import (
    Carousel, CarouselBreakpoint, CarouselElementWrapper, CaroselImageFolder
)


class CarouselBreakpointInline(admin.StackedInline):
    model = CarouselBreakpoint
    extra = 0


class CarouselPlugin(CMSPluginBase):
    '''
    Parent slider plugin.

    Any other plugin can be added as a child (as a slide), or you can use
    special plugins that generate a list of elements (see
    CarouselImageFolderPlugin below for one such example
    '''

    model = Carousel
    render_template = "cmsplugin_slick/carousel.djhtml"
    module = _('Slick Carousel')
    name = _('Slick Carousel')
    allow_children = True
    inlines = [CarouselBreakpointInline, ]

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'default_style',
                'infinite',
                'speed',
                'height',
                ('dots', 'arrows'),
                ('slides_to_show', 'slides_to_scroll'),
            )
        }),
        (_('Autoplay'), {
            'classes': ('collapse',),
            'fields': (
                ('autoplay', 'autoplay_speed'),
                ('pause_on_hover', 'pause_on_dots_hover'),
            )
        }),
        (_('Others Settings'), {
            'classes': ('collapse',),
            'fields': (
                'fade',
                ('center_mode', 'center_padding'),
                'variable_width',
                ('vertical', 'rigth_to_left'),
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse',),
            'fields': (
                'classes',
            )
        }),
        (_('Breakpoint Settings'), {
            'fields': (
                'auto_breakpoints', 'mobile_first',
            )
        }),
    )

    def make_auto_breakpoints(self, instance):
        # breakpoints (bootstrap):
        # xs:  480px [  0; 768-1]
        # sm:  768px [768; 992-1]
        # md:  992px [992; 1200-1]
        # lg: 1200px [1200; inf+]

        def slide_decr(x):
            return max(x-1, 1)

        def slide_incr(x):
            return max(x+1, 1)

        def media(breakpoint, slidesToShow=1, slidesToScroll=1, **kwargs):
            settings = {
                'slidesToShow': slidesToShow,
                'slidesToScroll': slidesToScroll,
            }
            settings.update(**kwargs)

            media_dict = {
                'breakpoint': breakpoint,
                'settings': settings,
            }
            return media_dict

        slides = instance.slides_to_show
        if instance.mobile_first:
            # default settings are xs
            # mobile-first, thus means:
            # 'from this breakpoint and above, do this'
            slides = slide_incr(slides)
            sm = media(768, slidesToShow=slides, slidesToScroll=1)

            slides = slide_incr(slides)
            md = media(992, slidesToShow=slides, slidesToScroll=1)

            responsive = [sm, md]

        else:
            # default settings are lg+
            # not mobile-first, thus means:
            # 'from this breakpoint and below, do this'
            # md = media(1200-1, slidesToShow=slides, slidesToScroll=1)
            slides = slide_decr(slides)
            md = media(1200-1, slidesToShow=slides, slidesToScroll=1)

            slides = slide_decr(slides)
            sm = media(992-1, slidesToShow=slides, slidesToScroll=1)

            # forcing 1 slide in xs
            xs = media(768-1, slidesToShow=1, slidesToScroll=1)

            responsive = [sm, xs, md]

        # output = {
        #     'responsive': responsive
        # }
        return responsive

    def render(self, context, instance, placeholder):
        context = super(CarouselPlugin, self).render(
            context, instance, placeholder)

        slick_dict = {
            'infinite': instance.infinite,
            'speed': instance.speed,
            'dots': instance.dots,
            'arrows': instance.arrows,
            'slidesToShow': instance.slides_to_show,
            'slidesToScroll': instance.slides_to_scroll,
            'autoplay': instance.autoplay,
            'autoplaySpeed': instance.autoplay_speed,
            'pauseOnHover': instance.pause_on_hover,
            'pauseOnDotsHover': instance.pause_on_dots_hover,
            'fade': instance.fade,
            'centerMode': instance.center_mode,
            'centerPadding': instance.center_padding,
            'variableWidth': instance.variable_width,
            'vertical': instance.vertical,
            'rtl': instance.rigth_to_left,
            'slide': ':not(template)',
        }

        if instance.auto_breakpoints:
            responsive = self.make_auto_breakpoints(instance)
            slick_dict.update({'responsive': responsive})
        else:
            if instance.breakpoints.all():
                responsive = []
                for breakpoint in instance.breakpoints.all():
                    responsive.append({
                        'breakpoint': breakpoint.breakpoint,
                        'settings': {
                            'slidesToShow': breakpoint.slides_to_show,
                            'slidesToScroll': breakpoint.slides_to_scroll
                        }
                    })

            slick_dict.update({'responsive': responsive})

        slick_settings = json.dumps(slick_dict)
        context.update({'slick_settings': slick_settings})
        return context


class CarouselElementWrapperPlugin(CMSPluginBase):
    '''
    Include all child plugin as one slide
    '''
    model = CarouselElementWrapper
    render_template = "cmsplugin_slick/element_wrapper.djhtml"
    module = 'Slick Carousel'
    name = _('Slide Wrapper')
    # require_parent = True
    parent_classes = ['CarouselPlugin']
    allow_children = True


class CarouselImageFolderPlugin(CMSPluginBase):
    model = CaroselImageFolder
    render_template = "cmsplugin_slick/folder_carousel.djhtml"
    module = 'Slick Carousel'
    name = _('Image Folder Carousel')
    # require_parent = True
    parent_classes = ['CarouselPlugin']

    fieldsets = (
        (None, {
            'fields': [
                'title',
                'folder',
            ]
        }),
        (_('Image resizing options'), {
            'fields': (
                'use_original_image',
                ('width', 'height',),
                ('crop', 'upscale',),
                'thumbnail_option',
                'use_autoscale',
            )
        }),
    )
    if settings.CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES:
        fieldsets[0][1]['fields'].append('style')

    def _get_thumbnail_options(self, context, instance):
        """
        Return the size and options of the thumbnail that should be inserted
        """
        width, height = None, None
        crop, upscale = False, False
        subject_location = False
        placeholder_width = context.get('width', None)
        placeholder_height = context.get('height', None)
        if instance.thumbnail_option:
            # thumbnail option overrides everything else
            if instance.thumbnail_option.width:
                width = instance.thumbnail_option.width
            if instance.thumbnail_option.height:
                height = instance.thumbnail_option.height
            crop = instance.thumbnail_option.crop
            upscale = instance.thumbnail_option.upscale
        else:
            if instance.use_autoscale and placeholder_width:
                # use the placeholder width as a hint for sizing
                width = int(placeholder_width)
            elif instance.width:
                width = instance.width
            if instance.use_autoscale and placeholder_height:
                height = int(placeholder_height)
            elif instance.height:
                height = instance.height
            crop = instance.crop
            upscale = instance.upscale

        if not width:
            width = 0
        if not height:
            height = 0

        return {
            'size': (width, height),
            'crop': crop,
            'upscale': upscale,
            'subject_location': subject_location,
        }

    def get_thumbnail(self, context, instance):
        if instance.image:
            return instance.image.file.get_thumbnail(self._get_thumbnail_options(context, instance))

    # def get_render_template(self, context, instance, placeholder):
    #     template = select_template((
    #         'cmsplugin_filer_image/plugins/image.html',  # backwards compatibility. deprecated!
    #         self.TEMPLATE_NAME % instance.style,
    #         self.TEMPLATE_NAME % 'default',
    #     ))
    #     return template

    # def icon_src(self, instance):
    #     if instance.image:
    #         if getattr(settings, 'FILER_IMAGE_USE_ICON', False) and '32' in instance.image.icons:
    #             return instance.image.icons['32']
    #         else:
    #             # Fake the context with a reasonable width value because it is not
    #             # available at this stage
    #             thumbnail = self.get_thumbnail({'width': 200}, instance)
    #             return thumbnail.url
    #     else:
    #         return static("filer/icons/missingfile_%sx%s.png" % (32, 32,))

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

        options = self._get_thumbnail_options(context, instance)
        context.update({
            'folder_images': sorted(folder_images),
            'instance': instance,
            'opts': options,
            'size': options.get('size', None),
            'placeholder': placeholder
            # 'link': instance.link,
        })
        return context


plugin_pool.register_plugin(CarouselPlugin)
plugin_pool.register_plugin(CarouselElementWrapperPlugin)
plugin_pool.register_plugin(CarouselImageFolderPlugin)
