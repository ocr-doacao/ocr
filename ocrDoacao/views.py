#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys, os
# from django.http import HttpResponse, Http404
from models import Ong, Imagem, NotaFiscal
from django.shortcuts import render
from django.db import IntegrityError

def index(request):
    o = Ong.objects.all()
    return render(request, 'inicial.html', {'onglist': o})

def erro_404(request):
    return render(request, '404.html')

def upload_image(request, ong):
    i = Imagem()
    try:
        i.save(fd=request.FILES['file1'], ong=ong)
    except IntegrityError:
        return render(request, 'resposta.html', {'ong': "", 'msg': "Falha ao salvar imagem!"})
    return render(request, 'resposta.html', {'ong': "", 'msg': "Imagem salva corretamente!"})

def ong_page(request, ongname):
    try:
        ong = Ong.objects.get(nome=ongname)
    except Ong.DoesNotExist:
        return render(request, '404.html')
    if request.method == "POST":
        return upload_image(request, ong)
    return render(request, 'ong.html')
