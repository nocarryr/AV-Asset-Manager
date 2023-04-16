"""avam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path, include
from django.contrib import admin

from site_navigation import urls as site_urls
from assets import urls as asset_urls
from object_history import urls as object_history_urls
from assettags import urls as assettags_urls
from categories import urls as categories_urls

urlpatterns = [
    path('', include(site_urls)),
    path('assets/', include(asset_urls)),
    path('admin/', admin.site.urls),
    path('object_history/', include(object_history_urls)),
    path('assettags/', include(assettags_urls)),
    path('categories/', include(categories_urls)),
]
