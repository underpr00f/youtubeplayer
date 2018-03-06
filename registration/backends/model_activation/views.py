#! /home/underproof/myvenv/bin python
# -*- coding:utf-8 -*-
"""
A two-step (registration followed by activation) workflow, implemented
by storing an activation key in a model and emailing the key to the
user.

This workflow is provided primarily for backwards-compatibility with
existing installations; new installs of django-registration should
look into the HMAC activation workflow in registration.backends.hmac.

"""

from django.contrib.sites.shortcuts import get_current_site

from registration import signals
from registration.models import RegistrationProfile
from registration.views import ActivationView as BaseActivationView
from registration.views import RegistrationView as BaseRegistrationView

#login|logout
from registration.views import LoginFormView as BaseLoginFormView
from registration.views import LogoutView as BaseLogoutView

#recover/reset pass
from registration.views import SaltMixin as BaseSaltMixin
from registration.views import RecoverDone as BaseRecoverDone
from registration.views import Recover as BaseRecover
from registration.views import Reset as BaseReset
from registration.views import ResetDone as BaseResetDone

from .utils import get_user_model, get_username

from registration.views import change_password
from registration.views import about_us
from registration.views import my_homepage_view

class RegistrationView(BaseRegistrationView):
    """
    Register a new (inactive) user account, generate and store an
    activation key, and email it to the user.

    """
    def register(self, form):
        new_user = RegistrationProfile.objects.create_inactive_user(
            form,
            site=get_current_site(self.request)
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def get_success_url(self, user):
        return ('registration_complete', (), {})


class ActivationView(BaseActivationView):
    """
    Given a valid activation key, activate the user's
    account. Otherwise, show an error message stating the account
    couldn't be activated.

    """
    def activate(self, *args, **kwargs):
        activation_key = kwargs.get('activation_key')
        activated_user = RegistrationProfile.objects.activate_user(
            activation_key
        )
        return activated_user

    def get_success_url(self, user):
        return ('registration_activation_complete', (), {})
'''
#переделать
class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    #template_name = "logout.html"
    
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")
'''
class LoginFormView(BaseLoginFormView):
    pass    
class LogoutView(BaseLogoutView):
    pass

class SaltMixin(BaseSaltMixin):
    pass    
class RecoverDone(BaseRecoverDone):
    pass
class Recover(BaseRecover):
    pass    
class Reset(BaseReset):
    pass
class ResetDone(BaseResetDone):
    pass    
'''
###Change password form
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
'''

