from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from filer.fields.folder import FilerFolderField
from filer.fields.file import FilerFileField


# Create your models here.'
class SlickCarousel(CMSPlugin):
    '''Store main settings for Slick Carousel'''
    title = models.CharField(verbose_name=_('Title'), max_length=128, blank=True)

    slick_preset = models.ForeignKey(
        'SlickCarouselPreset',
        verbose_name=_('Preset'),
        blank=True,
        null=True,
        default=1,
        on_delete=models.SET_NULL,
    )
    breakpoints = models.ForeignKey(
        'SlickCarouselBreakpointsPreset',
        verbose_name=_('Breakpoints'),
        blank=True,
        null=True,
        default=1,
        on_delete=models.SET_NULL,
    )

    #Advanced
    classes = models.TextField(verbose_name=_('CSS classes'), blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)

    class Meta:
        verbose_name = _("Slick Carousel")
        verbose_name_plural = _("Slick Carousels")


class SlickCarouselPreset(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)

    infinite = models.BooleanField(verbose_name=_('Infinite'), default=True)
    speed = models.PositiveIntegerField(verbose_name=_('Speed'), default=300)

    dots = models.BooleanField(verbose_name=_('Dots'), default=True)
    arrows = models.BooleanField(verbose_name=_('Arrows'), default=True)

    slides_to_show = models.PositiveIntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.PositiveIntegerField(verbose_name=_('Slides to scroll'), default=1)

    center_mode = models.BooleanField(verbose_name=_('Center mode'), default=False)
    center_padding = models.CharField(verbose_name=_('Center padding'), max_length=10, blank=True)

    #Autoplay
    autoplay = models.BooleanField(verbose_name=_('Autoplay'), default=False)
    autoplay_speed = models.PositiveIntegerField(verbose_name=_('Autoplay speed'), default=3000)

    pause_on_hover = models.BooleanField(verbose_name=_('Pause on hover'), default=True)
    pause_on_dots_hover = models.BooleanField(verbose_name=_('Pause on dots hover'), default=True)

    #Responce
    RESPOND_TO_CHOICES = (
        ('window', _('Window')),
        ('slider', _('Slider')),
        ('min', _('Smaller of the two')),
    )
    respond_to = models.CharField(
        _('Respond to'),
        choices=RESPOND_TO_CHOICES,
        default='window',
        max_length=6
    )
    mobile_first = models.BooleanField(
        default=True,
        verbose_name=_('Mobile First'),
        help_text=_('Responsive settings use mobile first calculation')
    )

    #Advanced
    fade = models.BooleanField(verbose_name=_('Fade animation'), default=False)

    rows = models.PositiveIntegerField(verbose_name=_('Rows'), default=1)
    slides_per_row = models.PositiveIntegerField(verbose_name=_('Slides per row'), default=1)

    center_mode = models.BooleanField(verbose_name=_('Center mode'), default=False)
    center_padding = models.CharField(verbose_name=_('Center padding'), max_length=10, blank=True)

    variable_width = models.BooleanField(verbose_name=_('Variable Width'), default=False)
    adaptive_height = models.BooleanField(verbose_name=_('Adaptive Height'), default=False)

    vertical = models.BooleanField(verbose_name=_('Vertical'), default=False)
    rigth_to_left = models.BooleanField(verbose_name=_('Right to left'), default=False)

    use_theme = models.BooleanField(_('Use Slick theme'), default=True)
    slick_theme = FilerFileField(verbose_name=_('Slick theme file'), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Slick Carousel Preset")
        verbose_name_plural = _("Slick Carousels Presets")


class SlickCarouselBreakpointsPreset(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)
    breakpoints = models.ManyToManyField(
        'SlickCarouselBreakpoint',
        verbose_name=_('Breakpoints'),
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Slick Carousel Breakpoint Preset")
        verbose_name_plural = _("Slick Carousels Breakpoints Presets")


class SlickCarouselBreakpoint(models.Model):
    '''
    Carousel breakpoints allow to create responsive carousels
    '''
    title = models.CharField(verbose_name=_('Title'), max_length=128, blank=True)

    breakpoint = models.PositiveIntegerField(verbose_name=_('Breakpoint resolution'))

    slides_to_show = models.PositiveIntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.PositiveIntegerField(verbose_name=_('Slides to scroll'), default=1)

    #Advanced
    dots = models.NullBooleanField(verbose_name=_('Dots'), null=True)
    arrows = models.NullBooleanField(verbose_name=_('Arrows'), null=True)

    center_mode = models.NullBooleanField(verbose_name=_('Center mode'), null=True)
    center_padding = models.CharField(verbose_name=_('Center padding'), max_length=10, blank=True)

    autoplay = models.NullBooleanField(verbose_name=_('Autoplay'), null=True)
    autoplay_speed = models.PositiveIntegerField(
        verbose_name=_('Autoplay speed'),
        blank=True,
        null=True
    )

    def __str__(self):
        if self.title:
            str = '{title}: {breakpoint}, {slides_to_show}, {slides_to_scroll}'.format(**self.__dict__)
        else:
            str = '{breakpoint}, {slides_to_show}, {slides_to_scroll}'.format(**self.__dict__)

        advanced = ('dots', 'arrows', 'center_mode', 'center_padding', 'autoplay', 'autoplay_speed')
        if any(self.__dict__[name] for name in advanced):
            advanced_str = ''
            for key in advanced:
                if self.__dict__[key]:
                    advanced_str = '{advanced_str}{key}: {value}; '.format(
                        **{'advanced_str': advanced_str, 'key': key, 'value': self.__dict__[key]}
                    )

            advanced_str = advanced_str.strip(' ;')

            str = '{str}; Advanced({advanced_str})'.format(
                **{'str': str, 'advanced_str': advanced_str}
            )

        return str

    class Meta:
        verbose_name = _('Slick Carousel Breakpoint')
        verbose_name_plural = _('Slick Carousels Breakpoints')


class SlickCarouselWrappedSlide(CMSPlugin):
    title = models.CharField(_("Plugin title"), max_length=128, blank=True)
    caption = models.CharField(_("Content caption"), max_length=256, blank=True)
    classes = models.TextField(verbose_name=_('CSS classes'), blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)

    class Meta:
        verbose_name = _('Wrapped Slide')
        verbose_name_plural = _('Wrapped Slides')


class SlickCarouselFolderImages(CMSPlugin):
    title = models.CharField(_("Title"), max_length=128, null=True, blank=True)
    folder = FilerFolderField(null=True, on_delete=models.SET_NULL)
    caption = models.BooleanField(_("Add caption"), default=False)

    #Image
    autoscale = models.BooleanField(
        _("Use automatic scaling"),
        default=True,
        help_text=_('fit the image to the size of the container'),
    )
    thumbnail = models.BooleanField(
        _("Use thumbnails"),
        default=True,
        help_text=_('accelerate page load and save mobile traffic.')
    )
    thumbnail_option = models.ForeignKey(
        'filer.ThumbnailOption',
        verbose_name=_("Thumbnail options"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    #Link
    original_link = models.BooleanField(_("Link to original image"), default=True)
    target_blank = models.BooleanField(_('Open link in new window'), default=False)

    #Advanced
    ORDERED_BY_CHOUSE =(
        ('id', _('ID')),
        ('original_filename', _('File name')),
        ('uploaded_at', _('Uploadet at')),
        ('modified_at', _('Modified at')),
    )
    ordered_by = models.CharField(
        _('Ordered by'),
        choices=ORDERED_BY_CHOUSE,
        default='original_filename',
        max_length=17
    )
    reverse_order = models.BooleanField(_('Reverse order'), default=False)
    classes = models.TextField(verbose_name=_('CSS classes'), blank=True)

    def __str__(self):
        if self.title:
            return self.title
        elif self.folder_id and self.folder.name:
            return self.folder.name
        else:
            return _('<empty>')

    class Meta:
        verbose_name = _('Carousel Folder Images')
        verbose_name_plural = _('Carousels Folders Images')