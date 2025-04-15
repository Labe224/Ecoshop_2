from rest_framework import serializers
from .models import Produits

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produits
        fields = "__all__"