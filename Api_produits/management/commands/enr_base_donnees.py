from django.core.management.base import BaseCommand
import json
from Api_produits.models import Produits

class Command(BaseCommand):
    help = "Commande pour enregistrer les produits dans la base de données"

    def add_arguments(self, parser):
        parser.add_argument("chemin_fichier", type=str, help="Chemin vers le fichier contenant les données")

    def handle(self, *args, **options):
        chemin = options['chemin_fichier']
        produits_a_creer = []
        noms_existants = set(Produits.objects.values_list('nom', flat=True))

        with open(chemin, "r", encoding='utf-8') as file:
            for ligne in file:
                data = json.loads(ligne)
                if data['indice_ecolo']<1:
                    data['indice_ecolo']=1
                if data['Nom'] not in noms_existants:
                    description = '\n'.join(f"{key} {item}" for key, item in data['description'].items())
                    produit = Produits(
                        nom=data['Nom'],
                        prix=data['Prix'],
                        image=data['image'],
                        lien_achat=data['url'],
                        description=description,
                        note=data['note'],
                        site_marchand="Amazon fr",
                        indice_ecolo=round(data['indice_ecolo'],3),
                        categorie=data['categorie'],
                        nb_point=int(100 / data['indice_ecolo']*100)
                    )
                    produits_a_creer.append(produit)

        if produits_a_creer:
            Produits.objects.bulk_create(produits_a_creer)
            self.stdout.write(self.style.SUCCESS(f"{len(produits_a_creer)} produits ont été enregistrés avec succès."))
        else:
            self.stdout.write(self.style.WARNING("Aucun nouveau produit à enregistrer."))
