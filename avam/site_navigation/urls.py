from django.conf.urls import url

from site_navigation import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
