from django.conf.urls import url

from categories import views

urlpatterns = [
    url(r'^list-for-objects/$',
        views.CategoriesForObjects.as_view(),
        name='list_for_objects',
    ),
    url(r'^list-for-objects/json/$',
        views.CategoriesForObjects.as_view(),
        {'json':True},
        name='list_for_objects_json',
    ),
]
