"""yolo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from management import urls as management_urls
# from teacher import urls as teacher_urls
from student import urls as student_urls
from learning import urls as learning_urls

urlpatterns = [
    url(r'^management/', include(management_urls, namespace='management',
                                 app_name='management')),
    # url(r'^teacher/', include(teacher_urls)),
    url(r'^', include(student_urls, namespace='student', app_name='student')),
    url(r'^account/', include(learning_urls, namespace='learning',
                              app_name='learning')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
