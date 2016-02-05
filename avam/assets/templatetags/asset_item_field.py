import sys
import numbers

from django.db import models
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

PY2 = sys.version_info.major == 2
if not PY2:
    basestring = str

@register.simple_tag(takes_context=True)
def asset_field_title(context):
    field_name = context['field_name']
    asset = context.get('asset')
    if asset is None:
        asset = context['asset_list'].first()
    asset_instance = asset.asset_instance
    f = asset_instance._meta.get_field(field_name)
    return f.verbose_name.title()

@register.simple_tag(takes_context=True)
def asset_item_field(context):
    field_name = context['field_name']
    asset = context['asset']
    asset_instance = asset.asset_instance
    field_val = getattr(asset, field_name, getattr(asset_instance, field_name))
    is_numeric = False
    if isinstance(field_val, numbers.Number):
        cell = str(field_val)
        is_numeric = True
    if isinstance(field_val, basestring):
        cell = field_val
    elif isinstance(field_val, bool):
        if field_val:
            cell = '<i class="material-icons">check_box</i>'
        else:
            cell = '<i class="material-icons">check_box_outline_blank</i>'
    elif isinstance(field_val, models.Model):
        try:
            url = field_val.get_absolute_url()
        except AttributeError:
            url = None
        if url is not None:
            cell = '<a href={0}>{1}</a>'.format(url, field_val)
        else:
            cell = str(field_val)
    else:
        cell = str(field_val)
    if is_numeric:
        td = '<td class="mdl-data-table__cell--non-numeric">'
    else:
        td = '<td>'
    h = ''.join([td, cell, '</td>'])
    return mark_safe(h)
