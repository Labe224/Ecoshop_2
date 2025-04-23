
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404
from Api_produits.models import Produits
from .models import HistoriqueCommande

from .models import HistoriqueCommande, HistoriqueRecherche
from .serializers import (
    InscriptionSerializer,
    ConnexionSerializer,
    HistoriqueCommandeSerializer,
    HistoriqueRechercheSerializer,
    ChangementMotDePasseSerializer,
    ReinitialisationMotDePasseSerializer,
    MiseAJourProfilSerializer
)


# Inscription
class InscriptionVue(APIView):
    permission_classes = [AllowAny]

    def post(self, requete):
        serializer = InscriptionSerializer(data=requete.data)
        print(serializer)
        if serializer.is_valid():
            utilisateur = serializer.save()
            return Response({"message": "Utilisateur inscrit avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Connexion
class ConnexionVue(APIView):
    permission_classes = [AllowAny]

    def post(self, requete):
        serializer = ConnexionSerializer(data=requete.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            mot_de_passe = serializer.validated_data['mot_de_passe']
            utilisateur = authenticate(request=requete, email=email, password=mot_de_passe)
            if utilisateur:
                jeton = RefreshToken.for_user(utilisateur)
                return Response({
                    'jeton_actualisation': str(jeton),
                    'jeton_acces': str(jeton.access_token),
                })
            return Response({"erreur": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Profil utilisateur
class ProfilVue(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requete):
        utilisateur = requete.user
        return Response({
            "nom_utilisateur": utilisateur.username,
            "email": utilisateur.email,
            "points": utilisateur.points,
        })


# Historique des commandes



class HistoriqueCommandeVue(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = HistoriqueCommandeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoriqueCommande.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        utilisateur = self.request.user
        nom_produit = self.request.data.get('nom_produit')

        try:
            produit = Produits.objects.get(nom=nom_produit)
            points_du_produit = produit.nb_point
        except Produits.DoesNotExist:
            points_du_produit = 0  # Aucun point si le produit est introuvable

        serializer.save(utilisateur=utilisateur)
        utilisateur.points += points_du_produit
        utilisateur.save()

class SupprimerCommandeParNomVue(generics.DestroyAPIView):
    serializer_class = HistoriqueCommandeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('id') 
        try:
            return HistoriqueCommande.objects.get(id=id, utilisateur=self.request.user)
        except HistoriqueCommande.DoesNotExist:
            raise Http404("Historique introuvable avec ce nom.")

# Historique des recherches
class HistoriqueRechercheVue(generics.ListCreateAPIView):
    serializer_class = HistoriqueRechercheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoriqueRecherche.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


# Changement de mot de passe
class ChangementMotDePasseVue(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, requete):
        serializer = ChangementMotDePasseSerializer(data=requete.data)
        if serializer.is_valid():
            utilisateur = requete.user
            if not utilisateur.check_password(serializer.validated_data['ancien_mot_de_passe']):
                return Response({"ancien_mot_de_passe": "Mot de passe actuel incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            utilisateur.set_password(serializer.validated_data['nouveau_mot_de_passe'])
            utilisateur.save()
            return Response({"message": "Mot de passe mis à jour avec succès"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Réinitialisation de mot de passe
class ReinitialisationMotDePasseVue(APIView):
    permission_classes = [AllowAny]

    def post(self, requete):
        serializer = ReinitialisationMotDePasseSerializer(data=requete.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mot de passe réinitialisé avec succès"}, status=200)
        return Response(serializer.errors, status=400)


# Mise à jour du profil
class MiseAJourProfilVue(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, requete):
        serializer = MiseAJourProfilSerializer(requete.user, data=requete.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil mis à jour avec succès"})
        return Response(serializer.errors, status=400)