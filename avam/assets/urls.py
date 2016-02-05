from django.conf.urls import url

from assets import views

urlpatterns = [
    url(r'^$',
        views.AssetList.as_view(),
        name='asset_list',
    ),
    url(r'^detail/(?P<pk>[0-9]+)/$',
        views.AssetDetail.as_view(),
        name='asset_detail',
    ),
]
