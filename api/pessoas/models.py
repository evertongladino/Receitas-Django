from django.db import models
from django.forms import CharField

class Pessoa(models.Model):
    nome = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.nome
