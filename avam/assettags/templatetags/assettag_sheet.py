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

@register.simple_tag(takes_context=True)
def assettag_new_page(context):
    lines = []
    if not context['forloop']['first']:
        lines.extend([
            '  </table>',
            '</div>',
        ])
    lines.extend([
        '<div class="tag-page">',
        '  <table class="tag-table">',
    ])
    return mark_safe('\n'.join(lines))

@register.simple_tag(takes_context=True)
def assettag_endfor(context):
    lines = [
        '    </tr>',
        '  </table>',
        '</div>',
    ]
    if context['use_pdf']:
        lines.append('<pdf:nextpage>')
    return mark_safe('\n'.join(lines))
