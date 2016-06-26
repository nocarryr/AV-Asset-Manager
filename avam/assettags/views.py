import json

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from assettags.models import (
    AssetTag,
    AssetTagImageTemplate,
    AssetTagPrintTemplate,
)
from assettags.forms import TagPrintForm, TagScanForm
from assettags.tag_handler import AssetTagImage
from assettags import inkscape_export

class AssetTagImageView(LoginRequiredMixin, DetailView):
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
    def render_to_response(self, context, **kwargs):
        if self.kwargs.get('as_file'):
            return HttpResponse(context['image'].qr_svg_bytes, content_type='image/svg+xml')
        return super(AssetTagImageView, self).render_to_response(context, **kwargs)


class AssetTagItemView(AssetTagImageView):
    template_name = 'assettags/assettag-item.html'
    slug_field = 'code'
    slug_url_kwarg = 'tag_code'

def asset_tag_form(request, **kwargs):
    tag = None
    if request.method == 'POST':
        form = TagScanForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['tagcode']
            try:
                tag = AssetTag.objects.get(code=code)
            except AssetTag.DoesNotExist:
                tag = None
    else:
        form = TagScanForm(**kwargs)
    return form, tag

@login_required
def asset_tag_lookup(request, **kwargs):
    def get_url_for_code(code=None, tag=None):
        if tag is None:
            tag = get_object_or_404(AssetTag, code=code)
        url = tag.get_asset_url()
        if url is None:
            url = reverse('assettags:assettag_item', kwargs={'tag_code':tag.code})
        return url
    code = kwargs.get('tag_code')
    if code is not None:
        return redirect(get_url_for_code(code))
    form, tag = asset_tag_form(request)
    if request.method == 'POST':
        if tag is not None:
            url = get_url_for_code(form.cleaned_data['tagcode'])
            return redirect(url)
    return render(request, 'assettags/qrscan.html', {'form':form})

@login_required
def asset_tag_assign(request, **kwargs):
    def get_content_data(formdata=None):
        instance = kwargs.get('instance')
        if instance is not None:
            content_type = ContentType.objects.get_for_model(instance._meta.model)
            ct_id = content_type.id
            object_id = instance.pk
        elif formdata is not None:
            ct_id = formdata['content_type_id']
            object_id = formdata['object_id']
            content_type = ContentType.objects.get_for_id(ct_id)
            m = content_type.model_class()
            instance = m.objects.get(pk=object_id)
        else:
            content_type = kwargs.get('content_type')
            if content_type is not None:
                ct_id = content_type.id
            else:
                ct_id = kwargs.get('content_type_id', request.GET.get('content_type_id'))
                try:
                    content_type = ContentType.objects.get_for_id(ct_id)
                except ContentType.DoesNotExist:
                    content_type = None
            object_id = kwargs.get('object_id', request.GET.get('object_id'))
            if content_type is not None:
                m = content_type.model_class()
                try:
                    instance = m.objects.get(pk=object_id)
                except m.DoesNotExist:
                    instance = None
        return dict(
            content_type=content_type,
            content_type_id=ct_id,
            object_id=object_id,
            instance=instance,
        )
    if request.method == 'POST':
        form, tag = asset_tag_form(request)
        if form.is_valid():
            data = get_content_data(form.cleaned_data)
            tag.assign_asset(data['instance'])
            messages.success(
                request,
                'Asset Tag %s successfully assigned to %s' % (tag, data['instance']),
            )
    else:
        data = get_content_data()
        keys = ['content_type_id', 'object_id']
        form, tag = asset_tag_form(request, initial={k:data[k] for k in keys})
    context = dict(
        form=form,
        header_text='Assign Tag for %s' % (data['instance']),
    )
    return render(request, 'assettags/assign-tag.html', context)

@login_required
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
            pdf_preview = data['pdf_preview']
            use_pdf = pdf_preview or data['render_as'] == 'pdf'
            if use_pdf:
                use_png = True
                if pdf_preview:
                    dpi = 96.
                else:
                    dpi = 96.
                page_box = page_tmpl.get_full_area(dpi)
                print_box = page_tmpl.get_printable_area(dpi)
                template_name = 'assettags/assettag-sheet.svg.html'
                root_tag = 'g'
            else:
                use_png = False
                dpi = 96.
                page_box = page_tmpl.get_full_area(dpi)
                print_box = page_tmpl.get_printable_area(dpi)
                template_name = 'assettags/assettag-table.html'
                root_tag = 'svg'
            cell = page_tmpl.get_cells(dpi)[0]
            tag_scale = [u.to_other('px') for u in [cell.w, cell.h]]
            tag_imgs = [AssetTagImage(asset_tag=t, template=tag_tmpl, scale=tag_scale, root_tag=root_tag) for t in q]
            context = dict(
                use_png=use_png,
                use_pdf=use_pdf,
                tag_template=tag_tmpl,
                page_template=page_tmpl,
                page_box=page_box,
                print_box=print_box,
                tag_box=cell,
                padding=page_tmpl.get_html_padding(dpi),
                cell_iter=data['page_template'].iter_page_row_col_cell(tag_imgs, dpi=dpi),
                dpi=dpi,
            )
            if use_pdf and not pdf_preview:
                return render_pdf(template_name, context)
            else:
                return render(request, template_name, context)
    else:
        form = TagPrintForm()
    template_map = {}
    for p_id, t_id in AssetTagPrintTemplate.objects.all().values_list('pk', 'asset_tag_template'):
        template_map[str(p_id)] = str(t_id)
    context = {
        'form':form,
        'template_map':json.dumps(template_map),
    }
    return render(request, 'assettags/print-tags.html', context)

def render_pdf(template_name, context_data):
    html = render_to_string(template_name, context_data)
    s = inkscape_export.render_from_html(html, context_data)
    return HttpResponse(s, content_type='application/pdf')
