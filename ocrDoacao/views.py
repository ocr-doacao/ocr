#!/usr/bin/python
# -*- coding: UTF8 -*-

from django.http import HttpResponse, Http404
from models import Ong, Imagem, Meta_imagem
from django.shortcuts import render
import pprint

def upload_image(request):
    pprint.pprint(request.FILES['file1'])
    return render(request, 'resposta.html', {'ong': "", 'msg': "Imagem salva corretamente!"})


def index(request):
    if request.method == "POST":
        return upload_image(request)
    return render(request, 'ong.html')