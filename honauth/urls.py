from django.urls import path
from .views import *


urlpatterns = [
    path('login/', HonLoginView.as_view(), name='login'),
    path('logout/', HonLogoutView.as_view(), name='logout'),
    path('settings/detail/<int:pk>', DetailHoNAppSettingsView.as_view(), name='settings_detail'),
    path('settigns/save/<int:pk>', CreateUpdateHoNAppSettings.as_view(), name='settings_save'),
]
