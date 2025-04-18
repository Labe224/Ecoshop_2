from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Modèle d'utilisateur 
class UtilisateurPersonnalise(AbstractUser):
    email = models.EmailField(unique=True)
    biographie = models.TextField(blank=True, null=True)
    email_verifie = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'


# Historique des commandes
class HistoriqueCommande(models.Model):
    utilisateur = models.ForeignKey(UtilisateurPersonnalise, on_delete=models.CASCADE, related_name='commandes')
    nom_produit = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField(default=1)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_produit} x{self.quantite} - {self.utilisateur.email}"


# Historique des recherches
class HistoriqueRecherche(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recherches")
    recherche = models.CharField(max_length=255)
    date_recherche = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.email} a recherché '{self.recherche}'"