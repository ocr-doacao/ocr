#!/usr/bin/python
# -*- coding: UTF8 -*-

import os
from django.db import models
import shutil

class Ong(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def get_path(self):
        mname = __name__.split(".")[0]
        return os.path.join(mname, "static", "ongs", self.nome)

    def save(self):
        os.makedirs(self.get_path(), 0744)
        return super(Ong, self).save()

    def delete(self):
        shutil.rmtree(self.get_path(), ignore_errors=True)
        return super(Ong, self).delete()