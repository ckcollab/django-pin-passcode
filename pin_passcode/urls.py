from django.urls import path

from . import views


urlpatterns = (
    path('pin', views.form, name='pin_form'),
    path('pin/auth', views.auth, name='pin_auth'),
    path('pin/test', views.test, name='pin_test'),
)
