from django.shortcuts import render
from django.views.generic import DetailView

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
            img_gen = AssetTagSheet(
                asset_tags=list(q),
                asset_tag_template=data['tag_template'],
                page_template=data['page_template'],
            )
            svgs = img_gen.build_all(as_string=True)
            return render(request, 'assettags/print-tags-result.html', {'svgs':svgs})
    else:
        form = TagPrintForm()
    return render(request, 'assettags/print-tags.html', {'form':form})
