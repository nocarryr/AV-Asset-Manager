from django.conf.urls import url

from assettags import views

urlpatterns = [
    url(r'^lookup/$', 
        views.asset_tag_lookup,
        name='assettag_lookup',
    ),
    url(r'^lookup/(?P<tag_code>[\w-]+)/$',
        views.asset_tag_lookup,
        name='assettag_lookup_coded',
    ),
    url(r'^assettag_item/(?P<tag_code>[\w-]+)/$',
        views.AssetTagItemView.as_view(),
        name='assettag_item',
    ),
    url(r'^assettag_image/(?P<pk>[0-9]+)/$',
        views.AssetTagImageView.as_view(),
        name='assettag_image',
    ),
    url(r'^print/$',
        views.print_tags,
        name='print_tags',
    ),
]
