from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^planning/(?P<pk>\d+)/?$', views.planning, name='planning'),
]
