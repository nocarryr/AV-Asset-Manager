from django.urls import path

from assets import views

app_name = 'assets'
urlpatterns = [
    path('',
        views.AssetList.as_view(),
        name='asset_list',
    ),
    path('detail/<int:pk>/',
        views.AssetDetail.as_view(),
        name='asset_detail',
    ),
]
