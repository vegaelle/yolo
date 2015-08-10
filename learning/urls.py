from django.conf.urls import url
from django.contrib.auth.views import login as login_url, logout as logout_url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='logged_out_home'),
    url(r'^login/?$', login_url, name='login'),
    url(r'^logout/?$', logout_url, name='logout'),
]
