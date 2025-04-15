from django.urls import path
from .views import *

urlpatterns = [
     path('produits/', Liste_produits.as_view(), name='liste-produits') 
]
