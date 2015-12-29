from django.views.generic import DetailView

from assettags.models import (
    AssetTag,
    AssetTagImageTemplate,
)
from assettags.tag_handler import AssetTagImage

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
