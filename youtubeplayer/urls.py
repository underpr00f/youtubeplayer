#! /home/underproof/myvenv/bin python
# -*- coding:utf-8 -*-
"""youtubeplayer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
import registration.views
#admin.autodiscover()
from django.views.decorators.cache import never_cache
from django.conf import settings
#from chat.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^sign_up/', player.views.register_user),
    #url(r'^register_success/', player.views.register_success),
    #url(r'^confirm/(?P<username>\w+)/', player.views.register_confirm),
    #url(r'^register/$', 'registration.views.register', {'form': RegistrationFormUniqueEmail}, name='registration_register'),

    url(r'^accounts/', include('registration.urls')),
    url(r'^$', never_cache(registration.views.my_homepage_view), name='home'), #корень сайта
    url(r'^socialprofile/', include('socialprofile.urls')),
    url(r'^chat/', include('chat.urls', namespace='chat_index')),
    url(r'^friendship/', include('friendship.urls', namespace='friend_index')),
    
    #url(r'^accounts/', include('socialprofile.urls', namespace="accounts")),

    # Index Page
    #url(r'^$', never_cache(IndexView.as_view()), name="sp_demo_home_page"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles import views as staticfiles_view
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', staticfiles_view.serve),
    ] 

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

