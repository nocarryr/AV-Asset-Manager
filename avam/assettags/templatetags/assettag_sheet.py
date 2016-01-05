from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def assettag_new_row(context):
    if context['forloop']['first']:
        s = '<tr>'
    else:
        s = '</tr>\n<tr>'
    return mark_safe(s)

#@register.simple_tag(takes_context=True)
#def assettag_new_page(context):
#    
