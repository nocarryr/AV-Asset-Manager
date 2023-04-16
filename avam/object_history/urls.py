from django.urls import path

from object_history import views

app_name = 'object_history'
urlpatterns = [
    path('object_history/<int:pk>/',
        views.ObjectHistory.as_view(),
        name='object_history',
    ),
]
