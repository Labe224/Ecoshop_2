from django.db import models
from django.contrib.auth.models import User

class Produits(models.Model):  # le modeles qui répresente nos produits 
    nom = models.CharField(max_length=245)
    prix = models.CharField(default=0)
    description=models.CharField(null=True)
    indice_ecolo = models.FloatField()
    image = models.URLField(null=True)
    note = models.CharField(default=0) # notes attribué par les acheteurs 
    site_marchand = models.URLField(null=True)
    categorie= models.CharField(max_length=245)
    nb_point = models.IntegerField(null=True)
    lien_achat=models.URLField(null=True)
    
    
    

    def __str__(self):
        return self.nom


