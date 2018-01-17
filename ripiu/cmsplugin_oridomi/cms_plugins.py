from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import __version__
from .models import OridomiPlugin

def panels(ints):
    result = [int(x) for x in ints.split(',')]
    if len(result) == 1:
        return result[0]
    return result

@plugin_pool.register_plugin
class OridomiPluginPublisher(CMSPluginBase):
    model = OridomiPlugin
    name = 'Oridomi'
    module = 'Ri+'
    render_template = 'ripiu/cmsplugin_oridomi/oridomi.html'
    allow_children = True
    fieldsets = (
        ('', {
            'fields': (
                ('vertical_panels', 'horizontal_panels'),
                'perspective',
                'shading',
                'speed',
                'max_angle',
                'ripple',
                'oridomi_class',
                'shading_intensity',
                'easing_method',
                'gap_nudge',
                'touch_enabled',
                'touch_sensitivity',
            ),
        }), (
            _('Callbacks'), {
                'description': _('Custom callbacks for touch/drag events. '
                                 'Each one is invoked with a relevant value '
                                 'so they can be used to manipulate objects '
                                 'outside of the OriDomi instance (e.g. '
                                 'sliding panels). x values are returned '
                                 'when folding left and right, y values for '
                                 'top and bottom. The second argument passed '
                                 'is the original touch or mouse event. '
                                 'These are empty functions by default.'),
                'fields': (
                    'touch_start_callback',
                    'touch_move_callback',
                    'touch_end_callback',
                ),
            }
        )
    )

    def render(self, context, instance, placeholder):
        import json
        context = super(OridomiPluginPublisher, self).render(
            context, instance, placeholder
        )
        oridomi_conf = {
            'vPanels': panels(instance.vertical_panels),
            'hPanels': panels(instance.horizontal_panels),
            'perspective': instance.perspective,
            'shading': instance.shading,
            'speed': instance.speed,
            'maxAngle': instance.max_angle,
            'ripple': instance.ripple,
            
            # Object of type 'Decimal' is not JSON serializable
            'shadingIntensity': str(instance.shading_intensity),
            
            'easingMethod': instance.easing_method,
            
            # Object of type 'Decimal' is not JSON serializable
            'gapNudge': str(instance.gap_nudge),
            
            'touchEnabled': instance.touch_enabled,
            
            # Object of type 'Decimal' is not JSON serializable
            'touchSensitivity': str(instance.touch_sensitivity),
        }
        if instance.oridomi_class:
            oridomi_conf['oriDomiClass'] = instance.oridomi_class
        if instance.touch_start_callback:
            oridomi_conf['touchStartCallback'] = instance.touch_start_callback
        if instance.touch_move_callback:
            oridomi_conf['touchMoveCallback'] = instance.touch_move_callback
        if instance.touch_end_callback:
            oridomi_conf['touchEndCallback'] = instance.touch_end_callback
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'version': __version__,
            'conf': mark_safe(json.dumps(oridomi_conf)),
        })
        return context
