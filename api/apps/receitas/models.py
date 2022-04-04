from django.db import models
from django.forms import CharField, DateField
from datetime import datetime
from django.contrib.auth.models import User

class Receita(models.Model):
    nome_receita = models.CharField(max_length=200)
    ingredientes = models.TextField()
    modo_de_preparo = models.TextField()
    tempo_de_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    date  = models.DateField(default=datetime.today)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    publicada = models.BooleanField(default=True)
    foto_publicada = models.ImageField(upload_to='fotos/%d/%m/%Y/', blank=True)

    def __str__(self):
        return self.nome_receita