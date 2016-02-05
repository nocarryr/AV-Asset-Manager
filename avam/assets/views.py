from django.views.generic import ListView, DetailView

from assets.models import (
    Asset,
)

class AssetList(ListView):
    model = Asset
    template_name = 'assets/asset-list.html'
    context_object_name = 'asset_list'
    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['asset_item_fields'] = [
            'asset_model',
            'location',
            'in_use',
            'retired',
        ]
        return context

class AssetDetail(DetailView):
    model = Asset
    template_name = 'assets/asset-detail.html'
    context_object_name = 'asset'
