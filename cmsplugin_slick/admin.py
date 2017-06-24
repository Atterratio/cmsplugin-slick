from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from filer.admin.fileadmin import FileAdmin

from .models import SlickCarouselPreset, SlickCarouselBreakpointsPreset, SlickCarouselBreakpoint


@admin.register(SlickCarouselPreset)
class SlickCarouselPresetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slick_theme',
                'infinite',
                'speed',
                ('dots', 'arrows'),
                ('slides_to_show', 'slides_to_scroll'),
                ('center_mode', 'center_padding'),
            )
        }),
        (_('Autoplay options'), {
            'fields': (
                ('autoplay', 'autoplay_speed'),
                ('pause_on_hover', 'pause_on_dots_hover'),
            )
        }),
        (_('Responce options'), {
            'classes': ('collapse',),
            'fields': (
                'mobile_first',
                'respond_to',
            )
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'fade',
                ('rows', 'slides_per_row'),
                ('center_mode', 'center_padding'),
                ('variable_width', 'adaptive_height'),
                ('vertical', 'rigth_to_left'),
                ('use_theme', 'slick_theme'),
            )
        }),
    )


@admin.register(SlickCarouselBreakpointsPreset)
class SlickCarouselBreakpointsPresetAdmin(admin.ModelAdmin):
    filter_horizontal = ('breakpoints',)


@admin.register(SlickCarouselBreakpoint)
class SlickCarouselBreakpointAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'title',
                'breakpoint',
                ('slides_to_show', 'slides_to_scroll'),
            ]
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                ('dots', 'arrows'),
                ('center_mode', 'center_padding'),
                ('autoplay', 'autoplay_speed'),
            )
        }),
    )