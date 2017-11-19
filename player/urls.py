"""
URLconf for registration and activation, using django-registration's
two-step model-based activation workflow.

"""

from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    
    url(r'^$', never_cache(login_required(views.PlayerView.as_view())), name='player'),
    
]
