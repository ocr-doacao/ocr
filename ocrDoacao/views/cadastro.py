#!/usr/bin/python
# -*- coding: UTF8 -*-

import datetime
from ..models.notafiscal import busca, pega_query, criterio_busca
from ..models import Ong, Imagem, NotaFiscal
from django.shortcuts import render, redirect

def save_cadastro(request):
    id = request.POST['id_nf']
    dados = request.POST
    nf = NotaFiscal.objects.get(id=id)
    campos_invalidos = validaCadastro(dados)
    if len(campos_invalidos) == 0:
        nf.atualiza(dados)
        return redirect("/ong/" + nf.imagem.ong.nome + "/cadastro/")
    else:
        ong = nf.imagem.ong
        (start, fday, now) = criterio_busca()
        count = pega_query(ong, start, fday, now).count()
        data = dados['data']
        return render(request, 'cadastro.html', {'nf': nf, 'count': count,
            'data': data, 'campos_invalidos': campos_invalidos})

def cadastro_page(request, ongname):
    if request.method == "POST":
        return save_cadastro(request)
    try:
        ong = Ong.objects.get(nome=ongname)
    except Ong.DoesNotExist:
        return redirect('/404/')
    (count, nf) = busca(ong)
    if count == 0:
        return render(request, 'resposta.html', {'ong': "", 'msg': "Parabéns, todas as notas foram salvas!"})
    return render(request, 'cadastro.html', {'nf': nf, 'count': count, 'data': nf.hora_atualizacao.strftime("%d/%m/%Y")})
    
def validaCadastro(dados):
    campos_invalidos = {}
    if NotaFiscal.validaCNPJ(dados['cnpj']) is not True:
        campos_invalidos['cnpj'] = '* CNPJ inválido'
    if NotaFiscal.validaCOO(dados['coo']) is not True:
        campos_invalidos['coo'] = '* COO inválido'
    if NotaFiscal.validaValor(dados['total']) is not True:
        campos_invalidos['total'] = '* Valor inválido'
    data_valida = NotaFiscal.validaData(dados['data'])
    if  data_valida == 0:
        campos_invalidos['data'] = '* Data inválida'
    if data_valida == 1:
        campos_invalidos['data'] = '* Data fora do prazo de doação'
    return campos_invalidos
    
def invalida_nota(request, ongname, nf_id):
    try:
        nf = NotaFiscal.objects.get(id=nf_id)
        nf.descarta()
    except NotaFiscal.DoesNotExist:
        pass
    return redirect('/ong/' + ongname + '/cadastro')