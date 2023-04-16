
from django.db import models
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

from ..models import GenericAsset

@register.simple_tag(takes_context=True)
def asset_field_title(context):
    field_name = context['field_name']
    if field_name.startswith('location'):
        if '__' in field_name:
            field_name = field_name.split('__')[-1]
        return field_name.title()
    asset = context.get('asset')
    if asset is None:
        asset = context['asset_list'].first()
        if asset is None:
            meta = GenericAsset._meta
        else:
            meta = asset.asset_instance._meta
    f = meta.get_field(field_name)
    return f.verbose_name.title()

@register.simple_tag(takes_context=True)
def asset_item_field(context):
    field_name = context['field_name']
    asset = context['asset']
    asset_instance = asset.asset_instance
    if field_name.startswith('location'):
        field_name = '__'.join([field_name, 'name'])
        lookup = field_name.split('__')
        lookup.reverse()
        obj = asset_instance
        while len(lookup):
            attr = lookup.pop()
            obj = getattr(obj, attr)
        field_val = obj
    else:
        field_val = getattr(asset, field_name, getattr(asset_instance, field_name))
    if isinstance(field_val, str):
        cell = field_val
    elif isinstance(field_val, bool):
        if field_val:
            cell = '<span class="octicon octicon-check"></span>'
        else:
            cell = '<span class="octicon octicon-dash"></span>'
    elif isinstance(field_val, models.Model):
        try:
            url = field_val.get_absolute_url()
        except AttributeError:
            url = None
        if url is not None:
            cell = '<a href={0}>{1}</a>'.format(url, field_val)
        else:
            cell = str(field_val)
        field_val = field_val.pk
    else:
        cell = str(field_val)
    attrs = {'data-fieldname':field_name, 'data-fieldvalue':field_val}
    attrs = ' '.join(['{0}="{1}"'.format(k, v) for k, v in attrs.items()])
    td = '<td {0}>'.format(attrs)
    h = ''.join([td, cell, '</td>'])
    return mark_safe(h)
