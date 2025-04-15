from .models import Produits
from rest_framework.response import Response
from .serialiezers import *
from rest_framework.views import APIView


class Liste_produits(APIView):
    def get(self,request):
        produits=Produits.objects.all()
        nom = request.query_params.get('nom')
        categorie = request.query_params.get('categorie')
        prix_max = request.query_params.get('prix_max')
        prix_min = request.query_params.get('prix_min')

        # Filtres conditionnels
        if nom:
            produits = produits.filter(nom__icontains=nom) # contient le mot
        if categorie:
            produits = produits.filter(categorie__iexact=categorie)
        if prix_max:
            produits = produits.filter(prix__lte=prix_max)
        if prix_min:
            produits = produits.filter(prix__gte=prix_min)

        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)
    
      
