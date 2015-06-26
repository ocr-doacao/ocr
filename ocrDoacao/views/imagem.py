#!/usr/bin/python
# -*- coding: UTF8 -*-

from ..models import Ong, Imagem, NotaFiscal
from django.shortcuts import render, redirect
from django.db import IntegrityError

def upload_image(request, ong):
    i = Imagem()
    
    try:
        i.save(fd=request.FILES['file1'], ong=ong)
    except IntegrityError:
        return render(request, 'ong.html', {'msgF': "Desculpe, essa imagem já foi enviada"})
    nf = NotaFiscal(imagem=i, ong=ong)
    try:
        nf.save()
    except IntegrityError:
        return render(request, 'ong.html',  {'msgF': "Falha ao salvar imagem!"})
    return render(request, 'ong.html', {'msgS': "Obrigado! Sua doação será de grande ajuda!"})

def ong_page(request, ongname):
    try:
        ong = Ong.objects.get(nome=ongname)
    except Ong.DoesNotExist:
        return redirect('/404/')
    if request.method == "POST":
        return upload_image(request, ong)
    return render(request, 'ong.html')