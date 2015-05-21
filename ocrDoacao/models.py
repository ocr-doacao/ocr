#!/usr/bin/python
# -*- coding: UTF8 -*-

from django.db import models

class Ong(models.Model):
    nome = models.CharField(max_length=50, unique=True)

class Imagem(models.Model):
    PREPROCESSAMENTO = 1
    PROCESSAMENTO = 2
    PROCESSADO = 3
    ESTADO_CHOICES = (
        (PREPROCESSAMENTO, 'Preprocessamento'),
        (PROCESSAMENTO, 'Processamento'),
        (PROCESSADO, 'Processado'),
    )
    ong = models.ForeignKey(Ong)
    path = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32)
    hora_envio = models.DateTimeField(auto_created=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=PREPROCESSAMENTO)
    foto = models.ImageField(upload_to="imagem", null=True, default=None)

class Meta_imagem(models.Model):
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