from django.urls import path

from categories import views

app_name = 'categories'
urlpatterns = [
    path('list-for-objects/',
        views.CategoriesForObjects.as_view(),
        name='list_for_objects',
    ),
    path('list-for-objects/json/',
        views.CategoriesForObjects.as_view(),
        {'json':True},
        name='list_for_objects_json',
    ),
]
