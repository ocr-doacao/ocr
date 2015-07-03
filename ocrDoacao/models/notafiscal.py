#!/usr/bin/python
# -*- coding: UTF8 -*-

import datetime

from django.db.models import Q
from django.db import models

from .ong import Ong
from .imagem import Imagem

class NotaFiscal(models.Model):
    SEMANALISE = 1
    ANALISANDO = 2
    VALIDO = 3
    INVALIDO = 4
    ESTADO_CHOICES = (
        (SEMANALISE, 'Não analisado'),
        (ANALISANDO, 'Analisando'),
        (VALIDO, 'Válido'),
        (INVALIDO, 'Inválido'),
    )
    imagem = models.OneToOneField(Imagem)
    ong = models.ForeignKey(Ong)
    coo = models.CharField(max_length=20, null=True)
    cnpj = models.CharField(max_length=20, null=True)
    data = models.DateField(auto_now=True, null=True)
    total = models.FloatField(null=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=SEMANALISE)
    hora_atualizacao = models.DateTimeField(auto_now=True)

    @staticmethod
    def validaCNPJ(cnpj):
        # defining some variables
        lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4 , 3, 2]
        lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # cleaning the cnpj
        cnpj = cnpj.replace( "-", "" )
        cnpj = cnpj.replace( ".", "" )
        cnpj = cnpj.replace( "/", "" )

        # finding out the digits
        verificadores = cnpj[-2:]

        # verifying the lenght of the cnpj
        if len( cnpj ) != 14:
            return False

        # calculating the first digit
        soma = 0
        id = 0
        for numero in cnpj:
            # to do not raise indexerrors
            try:
                lista_validacao_um[id]
            except:
                break

            soma += int( numero ) * int( lista_validacao_um[id] )
            id += 1

        soma = soma % 11
        if soma < 2:
            digito_um = 0
        else:
            digito_um = 11 - soma

        digito_um = str( digito_um ) # converting to string, for later comparison

        # calculating the second digit
        # suming the two lists
        soma = 0
        id = 0

        # suming the two lists
        for numero in cnpj:

            # to do not raise indexerrors
            try:
                lista_validacao_dois[id]
            except:
                break

            soma += int( numero ) * int( lista_validacao_dois[id] )
            id += 1

        # defining the digit
        soma = soma % 11
        if soma < 2:
            digito_dois = 0
        else:
            digito_dois = 11 - soma

        digito_dois = str( digito_dois )

        # returnig
        return bool( verificadores == digito_um + digito_dois )
    
    @staticmethod
    def validaCOO(coo):
        if len( coo ) != 6:
            return False
        if coo.isdigit() is not True:
            return False
        return True
    
    @staticmethod
    def validaValor(valor):
        try:
            valor = float(valor)
        except:
            return False
        if valor <= 0:
            return False
        return True
    
    @staticmethod
    def validaData(data):
        try:
            data_nf = datetime.datetime.strptime(data, '%d/%m/%Y')
        except:
            return 0
        hoje = datetime.datetime.now()
        if hoje.day < 20:
            if hoje.month > 1:
                primeiro_dia_valido = datetime.datetime(hoje.year, hoje.month - 1, 1)
            else:
                primeiro_dia_valido = datetime.datetime(hoje.year - 1, 12, 1)
        else:
            primeiro_dia_valido = datetime.datetime(hoje.year, hoje.month, 1)
        if primeiro_dia_valido <= data_nf <= hoje:
            return 2
        return 1
        
    def atualiza(self, dados):
        self.cnpj = dados['cnpj']
        self.coo = dados['coo']
        self.total = dados['total']
        self.estado = NotaFiscal.VALIDO
        self.data = datetime.datetime.strptime(dados['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
        self.save()
        
    def alteraEstado(self, estado, hora_atualizacao = None):
        if hora_atualizacao is not None:
            self.hora_atualizacao = hora_atualizacao
        self.estado = estado
        self.save()
    
    @staticmethod
    def busca(ong):
        (start, first_day, now) = NotaFiscal.criterio_busca()
        notas_sem_analise = NotaFiscal.notas_sem_analise(ong, start, first_day, now)
        count = NotaFiscal.total_notas_sem_analise(ong, start, first_day, now)
        if count == 0:
            return (0, None)
        nf = NotaFiscal.notas_sem_analise(ong, start, first_day, now).order_by('hora_atualizacao').all()[0]
        nf.alteraEstado(NotaFiscal.ANALISANDO, now)
        return (count, nf)

    @staticmethod
    def criterio_busca():
        now = datetime.datetime.now()
        start = now - datetime.timedelta(minutes=1)
        if now.day < 20:
            if now.month > 1:
                first_day = datetime.date(now.year, now.month - 1, 1)
            else:
                first_day = datetime.date(now.year - 1, 12, 1)
        else:
            first_day = datetime.date(now.year, now.month, 1)
        return (start, first_day, now)

    @staticmethod
    def total_notas_sem_analise(ong, start = None, first_day = None, now = None):
        if (start is None and first_day is None and now is None):
            (start, first_day, now) = NotaFiscal.criterio_busca()
        return NotaFiscal.notas_sem_analise(ong, start, first_day, now).count()

    @staticmethod
    def notas_sem_analise(ong, start, first_day, now):
        return NotaFiscal.objects.filter(
            Q(ong=ong, hora_atualizacao__gte=first_day, estado=NotaFiscal.SEMANALISE) |
            Q(ong=ong, hora_atualizacao__gte=first_day, hora_atualizacao__lte=start, estado=NotaFiscal.ANALISANDO)
        )

