from django.conf.urls import url

from assettags import views

urlpatterns = [
    url(r'^assettag_image/(?P<pk>[0-9]+)/$',
        views.AssetTagImageView.as_view(),
        name='assettag_image',
    ),
]
