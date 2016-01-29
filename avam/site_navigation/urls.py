from django.conf.urls import url

from django.contrib.auth import views as auth_views

from site_navigation import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/login/$', auth_views.login, name='account_login'),
    url(r'^accounts/logout/$',
        auth_views.logout,
        {'template_name':'registration/logged-out.html'},
        name='account_logout',
    ),
]
