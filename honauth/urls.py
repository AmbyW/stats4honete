from django.urls import path
from .views import *


urlpatterns = [
    path('login/', HonLoginView.as_view(), name='login'),
    path('logout/', HonLogoutView.as_view(), name='logout'),
]
