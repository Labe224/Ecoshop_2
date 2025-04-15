from django.db import models
from django.contrib.auth.models import User

class Commentaires(models.Model):   # models qui répresente le commentaire sur un produits 
    personne = models.CharField(max_length=450)
    texte = models.TextField()

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

class utilisateurs(models.Model):  # Abstract user pour tirer les informations de l'objet user de django
    nb_point = models.IntegerField()
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True)

class Panier(models.Model): # le models panier chaque utilisateurs ne peut avoir q'un seul panier 

    utilisateur = models.OneToOneField(utilisateurs, on_delete=models.CASCADE, related_name='panier') # on lie le panier à l'utilisateurs
    créé_le = models.DateTimeField(auto_now_add=True)


class ÉlémentPanier(models.Model):  # les élements du panier qui sont contenu dans le panier de l'utilisateur 
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='elements') # foreingkey permet de lié un un panier à plusieurs élements 
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantité = models.PositiveIntegerField(default=1)

    

    
