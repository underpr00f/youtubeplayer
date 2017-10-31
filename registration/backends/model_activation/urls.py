"""
URLconf for registration and activation, using django-registration's
two-step model-based activation workflow.

"""

from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache
from . import views


urlpatterns = [
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to
    # the view; that way it can return a sensible "invalid key"
    # message instead of a confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        views.ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        never_cache(views.RegistrationView.as_view()),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    url(r'', include('registration.auth_urls')),
    #url(r'^login/$', views.LoginFormView.as_view()),
    #url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^recover/(?P<signature>.+)/$', views.RecoverDone.as_view(),
        name='password_reset_sent'),
    url(r'^recover/$', views.Recover.as_view(), name='password_reset_recover'),
    url(r'^reset/done/$', views.ResetDone.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.Reset.as_view(),
        name='password_reset_reset'),
    url(r'^password/changing/$', never_cache(views.change_password), name='change_password'),
    url(r'^password/changing/done$', views.change_password, name='change_password_done'),
    
]
