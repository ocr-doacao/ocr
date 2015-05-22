#!/usr/bin/python
# -*- coding: UTF8 -*-

import datetime
from ..models.notafiscal import busca
from ..models import Ong, Imagem, NotaFiscal
from django.shortcuts import render, redirect

def save_cadastro(request):
    id = request.POST['id_nf']
    nf = NotaFiscal.objects.get(id=id)
    nf.cnpj = request.POST['cnpj']
    nf.coo = request.POST['coo']
    nf.total = request.POST['total']
    nf.estado = NotaFiscal.VALIDO
    nf.data = datetime.datetime.strptime(request.POST['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
    nf.save()
    return redirect("/ong/" + nf.imagem.ong.nome + "/cadastro/")

def cadastro_page(request, ongname):
    if request.method == "POST":
        return save_cadastro(request)
    try:
        ong = Ong.objects.get(nome=ongname)
    except Ong.DoesNotExist:
        return redirect('/404/')
    (count, nf) = busca(ong)
    if count == 0:
        return render(request, 'resposta.html', {'ong': "", 'msg': "Parabéns, todas as mensagens foram salvas!"})
    return render(request, 'cadastro.html', {'nf': nf, 'count': count, 'data': nf.hora_atualizacao.strftime("%d/%m/%Y")})