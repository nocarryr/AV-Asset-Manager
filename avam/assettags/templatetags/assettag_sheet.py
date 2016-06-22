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
    if context['use_pdf']:
        tag = 'svg'
        tag_attrs = dict(
            width=context['page_box'].w,
            height=context['page_box'].h,
            version='1.1',
            viewBox='0 0 {} {}'.format(context['page_box'].w.to_pixels().value, context['page_box'].h.to_pixels().value),
        )
    else:
        tag = 'table'
        tag_attrs = {'class':'tag-table'}
    lines = []
    if not context['forloop']['first']:
        lines.extend([
            '  </{}>'.format(tag),
            '</div>',
        ])
    attr_str = ' '.join(['{}="{}"'.format(k, v) for k, v in tag_attrs.items()])
    lines.extend([
        '<div class="tag-page">',
        '  <{} {}>'.format(tag, attr_str),
    ])
    return mark_safe('\n'.join(lines))

@register.simple_tag(takes_context=True)
def assettag_endfor(context):
    if context['use_pdf']:
        lines = [
            '    </svg>',
            '</div>',
            '<pdf:nextpage>'
        ]
    else:
        lines = [
            '    </tr>',
            '  </table>',
            '</div>',
        ]
    return mark_safe('\n'.join(lines))
