#!/usr/bin/python
# -*- coding: UTF8 -*-

import datetime

from django.db.models import Q
from django.db import models

from .ong import Ong
from .imagem import Imagem

def criterio_busca():
    now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=1)
    if now.day < 20:
        if now.month > 1:
            fday = datetime.date(now.year, now.month - 1, 1)
        else:
            fday = datetime.date(now.year - 1, 12, 1)
    else:
        fday = datetime.date(now.year, now.month, 1)
    return (start, fday, now)

def busca(ong):
    (start, fday, now) = criterio_busca()
    q = NotaFiscal.objects.filter(
        Q(ong=ong, hora_atualizacao__gte=fday, estado=NotaFiscal.SEMANALISE) |
        Q(ong=ong, hora_atualizacao__gte=fday, hora_atualizacao__lte=start, estado=NotaFiscal.ANALISANDO)
    )
    count = q.count()
    if count == 0:
        return (0, None)
    nf = q.order_by('hora_atualizacao').all()[0]
    nf.hora_atualizacao = now
    nf.estado = NotaFiscal.ANALISANDO
    nf.save()
    return (count, nf)


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