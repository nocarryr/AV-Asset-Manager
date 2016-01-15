try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView

from xhtml2pdf import pisa

from assettags.models import (
    AssetTag,
    AssetTagImageTemplate,
)
from assettags.forms import TagPrintForm
from assettags.tag_handler import AssetTagImage, AssetTagSheet

class AssetTagImageView(DetailView):
    model = AssetTag
    template_name = 'assettags/assettag-image.html'
    context_object_name = 'asset_tag'
    def get_context_data(self, **kwargs):
        context = super(AssetTagImageView, self).get_context_data(**kwargs)
        tmpl = AssetTagImageTemplate.get_default_template()
        img = AssetTagImage(asset_tag=context['object'], template=tmpl)
        context['image_template'] = tmpl
        context['image'] = img
        return context


class AssetTagItemView(AssetTagImageView):
    template_name = 'assettags/assettag-item.html'
    slug_field = 'code'
    slug_url_kwarg = 'tag_code'


def asset_tag_lookup(request, **kwargs):
    code = kwargs.get('tag_code')
    if code is None:
        return render(request, 'assettags/qrscan.html')
    tag = get_object_or_404(AssetTag, code=code)
    url = tag.get_asset_url()
    if url is None:
        return redirect('assettags:assettag_item', **kwargs)
    return redirect(url)


def print_tags(request):
    if request.method == 'POST':
        form = TagPrintForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            codes = set()
            if data['reprint_unassigned']:
                vl = AssetTag.objects.filter(object_id__isnull=True).values_list('code', flat=True)
                codes |= set(vl)
            if data['tags_to_create']:
                codes |= AssetTag.objects.generate_tags(data['tags_to_create'])
            q = AssetTag.objects.filter(code__in=codes)
            page_tmpl = data['page_template']
            tag_tmpl = data['tag_template']
            use_pdf = data['render_as'] == 'pdf'
            if use_pdf:
                use_png = True
                dpi = 72.
                page_box = page_tmpl.get_full_area(dpi)
                print_box = page_box
            else:
                use_png = False
                dpi = 96.
                page_box = page_tmpl.get_full_area(dpi)
                print_box = page_tmpl.get_printable_area(dpi)
            cell = page_tmpl.get_cells(dpi)[0]
            tag_tmpl = AssetTagImageTemplate.get_resized(tag_tmpl, width=cell.w, height=cell.h)
            tag_imgs = [AssetTagImage(asset_tag=t, template=tag_tmpl) for t in q]
            context = dict(
                use_png=use_png,
                use_pdf=use_pdf,
                tag_template=tag_tmpl,
                page_template=page_tmpl,
                page_box=page_box,
                print_box=print_box,
                padding=page_tmpl.get_html_padding(dpi),
                cell_iter=data['page_template'].iter_cells(tag_imgs),
            )
            template_name = 'assettags/assettag-table.html'
            if use_pdf:
                return render_pdf(template_name, context)
            else:
                return render(request, template_name, context)
    else:
        form = TagPrintForm()
    return render(request, 'assettags/print-tags.html', {'form':form})
    
def render_pdf(template_name, context_data):
    html = render_to_string(template_name, context_data)
    fh = StringIO()
    pdf = pisa.pisaDocument(html, dest=fh)
    r = HttpResponse(fh.getvalue(), content_type='application/pdf')
    fh.close()
    return r
