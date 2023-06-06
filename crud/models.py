from django.db import models

# Create your models here.
class Facultad(models.Model):
    idFacultad = models.AutoField(primary_key=True)
    facultad = models.CharField(max_length=100)
    femenino = models.IntegerField()
    masculino = models.IntegerField()
    anio = models.IntegerField()
    def __str__(self):
        texto = {0}
        return self.facultad
     
class TipoDiscapacidad(models.Model):
    idDiscapacidad = models.AutoField(primary_key=True)
    discapacidad = models.CharField(max_length=100)
    femenino = models.IntegerField()
    masculino = models.IntegerField()
    anio = models.IntegerField()
    def __str__(self):
        texto = {0}
        return self.discapacidad
    

    