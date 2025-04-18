from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import HistoriqueCommande, HistoriqueRecherche, UtilisateurPersonnalise

Utilisateur = get_user_model()

# Inscription
class InscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Utilisateur.objects.all())]
    )
    mot_de_passe = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmation_mot_de_passe = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = ('email', 'username', 'mot_de_passe', 'confirmation_mot_de_passe')

    def validate(self, donnees):
        if donnees['mot_de_passe'] != donnees['confirmation_mot_de_passe']:
            raise serializers.ValidationError({"mot_de_passe": "Les mots de passe ne correspondent pas."})
        return donnees

    def create(self, donnees_valides):
        donnees_valides.pop('confirmation_mot_de_passe')
        utilisateur = Utilisateur.objects.create_user(
            email=donnees_valides['email'],
            username=donnees_valides['username'],
            password=donnees_valides['mot_de_passe']
        )
        return utilisateur

# Connexion
class ConnexionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField()


# Historique des commandes
class HistoriqueCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueCommande
        fields = ['id', 'utilisateur', 'nom_produit', 'prix', 'date_commande']
        read_only_fields = ['utilisateur', 'date_commande']


# Historique des recherches
class HistoriqueRechercheSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueRecherche
        fields = ['id', 'recherche', 'date_recherche']


# Changement de mot de passe
class ChangementMotDePasseSerializer(serializers.Serializer):
    ancien_mot_de_passe = serializers.CharField(required=True)
    nouveau_mot_de_passe = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['ancien_mot_de_passe'] == attrs['nouveau_mot_de_passe']:
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")
        return attrs


# Réinitialisation de mot de passe 
class ReinitialisationMotDePasseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nouveau_mot_de_passe = serializers.CharField(write_only=True)

    def validate_email(self, valeur):
        if not Utilisateur.objects.filter(email=valeur).exists():
            raise serializers.ValidationError("Aucun utilisateur avec cet e-mail.")
        return valeur

    def save(self):
        email = self.validated_data["email"]
        mot_de_passe = self.validated_data["nouveau_mot_de_passe"]
        utilisateur = Utilisateur.objects.get(email=email)
        utilisateur.set_password(mot_de_passe)
        utilisateur.save()
        return utilisateur


# Mise à jour du profil
class MiseAJourProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilisateurPersonnalise
        fields = ['username', 'email', 'biographie']
        extra_kwargs = {'email': {'read_only': True}}