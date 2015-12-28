from django.conf.urls import url

from object_history import views

urlpatterns = [
    url(r'^object_history/(?P<pk>[0-9]+)/$',
        views.ObjectHistory.as_view(),
        name='object_history',
    ),
]
