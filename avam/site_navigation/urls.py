from django.urls import path

from django.contrib.auth import views as auth_views

from site_navigation import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'template_name':'registration/logged-out.html'},
        name='account_logout',
    ),
]
