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
    url(r'^assign/$',
        views.asset_tag_assign,
        name='asset_tag_assign_form',
    ),
    url(r'^assign/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        views.asset_tag_assign,
        name='asset_tag_assign',
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
