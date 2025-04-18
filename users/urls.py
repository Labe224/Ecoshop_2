from django.urls import path
from .views import (
    InscriptionVue,
    ConnexionVue,
    ProfilVue,
    HistoriqueCommandeVue,
    HistoriqueRechercheVue,
    ChangementMotDePasseVue,
    ReinitialisationMotDePasseVue,
    MiseAJourProfilVue
)

urlpatterns = [
    path('inscription/', InscriptionVue.as_view(), name='inscription'),
    path('connexion/', ConnexionVue.as_view(), name='connexion'),
    path('profil/', ProfilVue.as_view(), name='profil'),
    path('commandes/', HistoriqueCommandeVue.as_view(), name='historique-commandes'),
    path('recherches/', HistoriqueRechercheVue.as_view(), name='historique-recherches'),
    path('changer-mot-de-passe/', ChangementMotDePasseVue.as_view(), name='changer-mot-de-passe'),
    path('reinitialiser-mot-de-passe/', ReinitialisationMotDePasseVue.as_view(), name='reinitialiser-mot-de-passe'),
    path('modifier-profil/', MiseAJourProfilVue.as_view(), name='modifier-profil'),
]