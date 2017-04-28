from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from filer.fields.folder import FilerFolderField

from cmsplugin_filer_image.conf import settings


# Create your models here.
class Carousel(CMSPlugin):
    '''
    Store main settings for carousel
    '''

    class Meta:
        verbose_name = _('Carousel')
        verbose_name_plural = _('Carousels')

    title = models.CharField(verbose_name=_('Title'), max_length=60, blank=True)
    default_style = models.BooleanField(verbose_name=_('Use default style'), default=True)
    infinite = models.BooleanField(verbose_name=_('Infinite'), default=True)
    speed = models.IntegerField(verbose_name=_('Speed'), default=300)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)

    dots = models.BooleanField(verbose_name=_('Dots'), default=True)
    arrows = models.BooleanField(verbose_name=_('Arrows'), default=True)

    slides_to_show = models.IntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.IntegerField(verbose_name=_('Slides to scroll'), default=1)

    # Autoplay
    autoplay = models.BooleanField(verbose_name=_('Autoplay'), default=False)
    autoplay_speed = models.IntegerField(verbose_name=_('Autoplay speed'), null=True, blank=True)

    pause_on_hover = models.BooleanField(verbose_name=_('Pause on hover'), default=True)
    pause_on_dots_hover = models.BooleanField(verbose_name=_('Pause on dots hover'), default=False)

    # Other
    fade = models.BooleanField(verbose_name=_('Fade animation'), default=False)

    center_mode = models.BooleanField(verbose_name=_('Center mode'), default=False)
    center_padding = models.CharField(verbose_name=_('Center padding'), max_length=10, blank=True)

    variable_width = models.BooleanField(verbose_name=_('Variable Width'), default=False)

    vertical = models.BooleanField(verbose_name=_('Vertical'), default=False)
    rigth_to_left = models.BooleanField(verbose_name=_('Right to left'), default=False)


    # Advanced
    classes = models.TextField(verbose_name=_('Css classes'), blank=True)
    auto_breakpoints = models.BooleanField(verbose_name=_('Auto Breakpoints'), default=True)
    mobile_first = models.BooleanField(
        default=False,
        verbose_name=_('Mobile First'),
        help_text=_('Responsive settings use mobile first calculation')
    )


    def copy_relations(self, oldinstance):
        self.breakpoints = oldinstance.breakpoints.all()


class CarouselBreakpoint(models.Model):
    """
    Carousel breakpoints allow to create responsive carousels
    """
    carousel = models.ForeignKey('Carousel', related_name='breakpoints', verbose_name=_('Carousel'))
    breakpoint = models.IntegerField(verbose_name=_('Breakpoint resolution'))
    slides_to_show = models.IntegerField(verbose_name=_('Slides to show'), default=1)
    slides_to_scroll = models.IntegerField(verbose_name=_('Slides to scroll'), default=1)

    class Meta:
        verbose_name = _('Carousel Breakpoint')
        verbose_name_plural = _('Carousel Breakpoints')


class CarouselElementWrapper(CMSPlugin):
    classes = models.TextField(verbose_name=_('Css classes'), blank=True)

    class Meta:
        verbose_name = _('Carousel Slide')
        verbose_name_plural = _('Carousel Slides')


class CaroselImageFolder(CMSPlugin):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    FLOAT_CHOICES = ((LEFT, _("left")),
                     (RIGHT, _("right")),
                     (CENTER, _("center")),
                     )
    STYLE_CHOICES = settings.CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES
    DEFAULT_STYLE = settings.CMSPLUGIN_FILER_IMAGE_DEFAULT_STYLE
    EXCLUDED_KEYS = ['class', 'href', 'target', ]

    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    folder = FilerFolderField(null=True, on_delete=models.SET_NULL)

    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES, default=DEFAULT_STYLE, max_length=50, blank=True)
    # caption_text = models.CharField(_("caption text"), null=True, blank=True, max_length=255)
    alt_text = models.CharField(_("alt text"), null=True, blank=True, max_length=255)
    use_original_image = models.BooleanField(
        _("use the original image"), default=False,
        help_text=_('do not resize the image. use the original image instead.'))
    thumbnail_option = models.ForeignKey(
        'filer.ThumbnailOption', null=True, blank=True, verbose_name=_("thumbnail option"),
        help_text=_('overrides width, height, crop and upscale with values from the selected thumbnail option'))
    use_autoscale = models.BooleanField(_("use automatic scaling"), default=False,
                                        help_text=_('tries to auto scale the image based on the placeholder context'))
    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    crop = models.BooleanField(_("crop"), default=True)
    upscale = models.BooleanField(_("upscale"), default=True)
    # alignment = models.CharField(_("image alignment"), max_length=10, blank=True, null=True, choices=FLOAT_CHOICES)

    # free_link = models.CharField(_("link"), max_length=2000, blank=True, null=True,
    #                              help_text=_("if present image will be clickable"))
    # page_link = PageField(null=True, blank=True,
    #                       help_text=_("if present image will be clickable"),
    #                       verbose_name=_("page link"))
    # file_link = FilerFileField(
    #     null=True,
    #     blank=True,
    #     default=None,
    #     verbose_name=_("file link"),
    #     help_text=_("if present image will be clickable"),
    #     related_name='+',
    #     on_delete=models.SET_NULL,
    # )
    # original_link = models.BooleanField(_("link original image"), default=False,
    #                                     help_text=_("if present image will be clickable"))
    # description = models.TextField(_("description"), blank=True, null=True)
    # target_blank = models.BooleanField(_('Open link in new window'), default=False)
    # link_attributes = AttributesField(excluded_keys=EXCLUDED_KEYS, blank=True,
    #                                   help_text=_('Optional. Adds HTML attributes to the rendered link.'))
    # cmsplugin_ptr = models.OneToOneField(
    #     to=CMSPlugin,
    #     related_name='%(app_label)s_%(class)s',
    #     parent_link=True,
    # )

    # we only add the image to select_related. page_link and file_link are FKs
    # as well, but they are not used often enough to warrant the impact of two
    # additional LEFT OUTER JOINs.
    # objects = FilerPluginManager(select_related=('image',))

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        if self.title:
            return self.title
        elif self.folder_id and self.folder.name:
            return self.folder.name
        return _("<empty>")

    class Meta:
        verbose_name = _('Carousel Image Folder')
        verbose_name_plural = _('Image Folder Carousels')
