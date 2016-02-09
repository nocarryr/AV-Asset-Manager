from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from assets.models import (
    Asset,
)
from assets import forms

class AssetList(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets/asset-list.html'
    context_object_name = 'asset_list'
    def get_manufacturers(self, context):
        assets = [asset.asset_instance for asset in context['asset_list']]
        return set([asset.asset_model.manufacturer for asset in assets])
    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['manufacturers'] = self.get_manufacturers(context)
        context['asset_item_fields'] = [
            'asset_model',
            'location',
            'in_use',
            'retired',
        ]
        return context

class AssetDetail(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset-detail.html'
    context_object_name = 'asset'
    def get_context_data(self, **kwargs):
        context = super(AssetDetail, self).get_context_data(**kwargs)
        asset = context['asset'].asset_instance
        model_form = forms.build_model_form(instance=asset)
        if self.request.method == 'POST':
            context['asset_form'] = model_form(self.request.POST, instance=asset)
        elif self.request.method == 'GET':
            context['asset_form'] = model_form(instance=asset)
        return context
