"""ocrDoacao URL Configuration

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

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^404/?$', 'ocrDoacao.views.erro_404'),
    url(r'^ong/(?P<ongname>\w{0,50})/cadastro/?$', 'ocrDoacao.views.cadastro_page'),
    url(r'^ong/(?P<ongname>\w{0,50})/?$', 'ocrDoacao.views.ong_page', name='ong-page'),
    url(r'^ong/(?P<ongname>\w{0,50})/invalidar/(?P<nf_id>\d+)/?$', 'ocrDoacao.views.invalida_nota', name='invalida-nota'),
    url(r'^$', 'ocrDoacao.views.index'),
]
