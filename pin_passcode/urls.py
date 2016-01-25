from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'pin/$', views.form, name='pin_form'),
    url(r'pin/auth$', views.auth, name='pin_auth'),
    url(r'pin/test$', views.test, name='pin_test'),
)
