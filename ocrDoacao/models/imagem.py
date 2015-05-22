#!/usr/bin/python
# -*- coding: UTF8 -*-

import os
from django.db import models
import shutil
from hashlib import md5
from uuid import uuid4
from datetime import datetime
from .ong import Ong

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import IntegrityError

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
    md5 = models.CharField(max_length=32, unique=True)
    hora_envio = models.DateTimeField(auto_created=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=PREPROCESSAMENTO)

    def save(self, fd, ong):
        print "\n\n"
        mname = __name__.split(".")[0]
        fname, fext = os.path.splitext(fd.name)
        content = fd.read()
        self.md5 = md5(content).hexdigest()
        self.ong = ong
        self.hora_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.path = os.path.join(str(uuid4()))
        complete_path = os.path.join(mname, "static", "ongs", ong.nome, self.path)
        os.makedirs(complete_path, 0744)
        self.path = os.path.join(self.path, "img" + fext)
        path = default_storage.save(os.path.join(complete_path, "img" + fext), ContentFile(content))
        os.path.join(settings.MEDIA_ROOT, path)
        try:
            return super(Imagem, self).save()
        except IntegrityError as e:
            shutil.rmtree(complete_path)
            raise e