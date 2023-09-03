from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import RedirectURLMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView, DetailView, UpdateView
from django.views.generic.edit import BaseFormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login as login_func
from django.contrib.auth import logout as logout_func
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import HonStatSettings
from .forms import HonStatSettingsForm


class HonLoginView(BaseFormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    next_page = None

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login_func(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for field, errors in form.errors.as_data().items():
            for error in errors:
                for err in error:
                    messages.add_message(request=self.request,
                                         level=messages.ERROR,
                                         message=err)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.next_page:
            return str(self.next_page)
        return str(self.success_url)


class HonLogoutView(RedirectURLMixin, RedirectView):
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        logout_func(request)
        redirect_to = self.get_success_url()
        return HttpResponseRedirect(redirect_to)

    get = post

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        return self.success_url


class DetailHoNAppSettingsView(LoginRequiredMixin, DetailView):

    queryset = HonStatSettings.objects.all()
    model = HonStatSettings
    template_name = 'honauth/DetailSettings.html'
    context_object_name = 'hon_app_settings'

    def get_object(self, queryset=None):
        qr = queryset or self.queryset
        obj, created = qr.get_or_create(id=1)
        return obj


class CreateUpdateHoNAppSettings(LoginRequiredMixin, UpdateView):

    queryset = HonStatSettings.objects.all()
    model = HonStatSettings
    template_name = 'honauth/FormSettings.html'
    form_class = HonStatSettingsForm
    success_url = reverse_lazy('settings_detail', kwargs={'pk': 0})

    def get_object(self, queryset=None):
        qr = queryset or self.queryset
        obj, created = qr.get_or_create(id=1)
        return obj
