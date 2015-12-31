# coding=utf-8
"""peber_ex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# Image of the Day 
from django.conf import settings
from django.conf.urls.static import static

# DRF Needs
from peber_web import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'update_user_desc', views.UpdateUserDescViewSet)
router.register(r'news', views.NewsViewSet, 'News')
router.register(r'news_source', views.NewsSourceViewSet, 'News_Source')
router.register(r'user', views.UserViewSet, 'User')
router.register(r'user_desc', views.UserDescViewSet)
router.register(r'periodic_task', views.PeriodicTaskViewSet, 'PeriodicTask')


urlpatterns = [
    url(r'^peber_web/', include('peber_web.urls', namespace="peber_web")),  # Langsung dari root, 127.0.0.1/
    url(r'^accounts/', include('userprofile.urls', namespace="userprofile")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^peber_api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # URL pembantu untuk gambar (media URL)
