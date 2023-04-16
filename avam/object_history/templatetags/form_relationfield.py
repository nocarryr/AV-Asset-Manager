from django import template
from django.utils.encoding import smart_str
from django.db import models

register = template.Library()

@register.simple_tag
def related_obj_data(form, field):
    obj = form.initial[field.name]
    if not isinstance(obj, models.Model):
        return dict(label=obj, href=None)
    lbl = smart_str(obj)
    if hasattr(obj, 'get_absolute_url'):
        href = obj.get_absolute_url()
    else:
        href = '#'
    return dict(label=lbl, href=href)
    
    
