#!/usr/bin/python
# -*- coding: UTF8 -*-

from ..models import Ong
from django.shortcuts import render, redirect
from .imagem import upload_image, ong_page
from .cadastro import cadastro_page, save_cadastro, invalida_nota

def index(request):
    o = Ong.objects.all()
    return render(request, 'inicial.html', {'onglist': o})

def erro_404(request):
    return render(request, '404.html')