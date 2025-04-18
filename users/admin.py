
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UtilisateurPersonnalise

# Enregistrement du modèle utilisateur

class UtilisateurAdmin(UserAdmin):
    model = UtilisateurPersonnalise
    list_display = ['email', 'username', 'email_verifie', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('biographie', 'email_verifie')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('biographie', 'email_verifie')}),
    )

admin.site.register(UtilisateurPersonnalise, UtilisateurAdmin)