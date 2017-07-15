from django.conf.urls import include, url
from . import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    url(r'^$',  never_cache(views.about), name='about'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^list_rooms/$', views.chat_list_rooms, name='chat_list_rooms'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),

]
