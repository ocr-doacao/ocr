#!/usr/bin/python
# -*- coding: UTF8 -*-

from django.db import models

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
    imagem = models.ForeignKey(Imagem)
    coo = models.CharField(max_length=20, null=True)
    cnpj = models.CharField(max_length=20, null=True)
    data = models.DateField(auto_now=True, null=True)
    total = models.FloatField(null=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=SEMANALISE)
    hora_atualizacao = models.DateTimeField(auto_now=True)