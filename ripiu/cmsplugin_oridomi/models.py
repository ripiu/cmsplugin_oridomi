from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator, validate_comma_separated_integer_list
)
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin


class OridomiPlugin(CMSPlugin):
    '''Oridomi container'''

    SHADING_HARD = 'hard'
    SHADING_SOFT = 'soft'
    SHADING_DISABLED = 'false'
    SHADING_CHOICES = (
        (SHADING_DISABLED, _('disabled')),
        (SHADING_HARD, _('hard')),
        (SHADING_SOFT, _('soft')),
    )

    RIPPLE_DISABLED = 0
    RIPPLE_FORWARD = 1
    RIPPLE_BACKWARDS = 2
    RIPPLE_CHOICES = (
        (RIPPLE_DISABLED, _('disabled')),
        (RIPPLE_FORWARD, _('forward')),
        (RIPPLE_BACKWARDS, _('backwards')),
    )

    vertical_panels = models.CharField(
        _('vertical panels'), max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=False, default='3',
        help_text=_('The number of vertical panels (for folding left or '
                    'right). You can use either an integer, or an array of '
                    'percentages if you want custom panel widths, e.g. 20, '
                    '10, 10, 20, 10, 20, 10. The numbers must add up to 100 '
                    '(or near it, so you can use values like 33, 33, 33).')
    )

    horizontal_panels = models.CharField(
        _('horizontal panels'), max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=False, default='3',
        help_text=_('The number of horizontal panels (for folding top or '
                    'bottom) or an array of percentages.')
    )

    perspective = models.PositiveSmallIntegerField(
        _('perspective'),
        blank=False, null=False, default=1000,
        help_text=_('The determines the distance in pixels (z axis) of the '
                    'camera/viewer to the paper. The smaller the value, the '
                    'more distorted and exaggerated the effects will appear.')
    )

    shading = models.CharField(
        _('shading'), max_length=255,
        choices=SHADING_CHOICES, default=SHADING_HARD,
        help_text=_("The default shading style is hard, which shows distinct "
                    "creases in the paper. Other options include 'soft' — for "
                    "a smoother, more rounded look — or false to disable "
                    "shading altogether for a flat look.")
    )

    speed = models.PositiveSmallIntegerField(
        _('speed'),
        blank=False, null=False, default=700,
        help_text=_('Determines the duration of all animations in '
                    'milliseconds.')
    )

    max_angle = models.PositiveSmallIntegerField(
        _('maximum angle'),
        blank=False, null=False, default=90,
        help_text=_('Configurable maximum angle for effects. With most '
                    'effects, exceeding 90/-90 usually makes the element wrap '
                    'around and pass through itself leading to some glitchy '
                    'visuals.')
    )

    ripple = models.PositiveSmallIntegerField(
        _('ripple'),
        blank=False, null=False,
        choices=RIPPLE_CHOICES, default=RIPPLE_DISABLED,
        help_text=_('Ripple mode causes effects to fold in a staggered, '
                    'cascading manner. 1 indicates a forward cascade, 2 is '
                    'backwards. It is disabled by default.')
    )

    oridomi_class = models.CharField(
        _('Oridomi class'), max_length=100,
        blank=True, default='',
        help_text=_('This CSS class is applied to OriDomi elements so they '
                    'can be easily targeted later.')
    )

    shading_intensity = models.DecimalField(
        _('shading intensity'),
        max_digits=3, decimal_places=2,
        blank=False, null=False, default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_('This is a multiplier that determines the darkness of '
                    'shading. If you need subtler shading, set this to a '
                    'value below 1.')
    )

    # TODO: write a validator for this
    easing_method = models.CharField(
        _('easing method'), max_length=255,
        blank=True, default='',
        help_text=_('This option allows you to supply the name of a CSS '
                    'easing method or a cubic bezier formula for customized '
                    'animation easing.')
    )

    gap_nudge = models.DecimalField(
        _('gap nudge'),
        max_digits=3, decimal_places=1,
        blank=False, null=False, default=1.5,
        validators=[MinValueValidator(0)],
        help_text=_('Number of pixels to offset each panel to prevent small '
                    'gaps from appearing between them. This is configurable '
                    'if you have a need for precision.')
    )

    touch_enabled = models.BooleanField(
        _('touch enabled'), default=True,
        help_text=_('Allows the user to fold the element via touch or mouse.')
    )

    touch_sensitivity = models.DecimalField(
        _('touch sensitivity'),
        max_digits=4, decimal_places=2,
        blank=False, null=False, default=0.25,
        help_text=_('Coefficient of touch/drag action’s distance delta. '
                    'Higher numbers cause more movement.')
    )

    touch_start_callback = models.CharField(
        _('touchstart callback'),
        max_length=255, blank=True,
        help_text=_('Invoked with starting coordinate as first argument.')
    )

    touch_move_callback = models.CharField(
        _('touchmove callback'),
        max_length=255, blank=True,
        help_text=_('Invoked with the folded angle.')
    )

    touch_end_callback = models.CharField(
        _('touchend callback'),
        max_length=255, blank=True,
        help_text=_('Invoked with ending point.')
    )

    def __str__(self):
        return str(_('(%(columns)s, %(rows)s)' % {
            'columns': self.vertical_panels,
            'rows': self.horizontal_panels,
        }))

    class Meta:
        verbose_name = _('Oridomi container')
        verbose_name_plural = _('Oridomi containers')
