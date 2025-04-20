import json
import requests

from calcul_ecolo  import *


"""Programme qui permet d'extraire les produits les adaptés au modele de la base de données et les enregistrer dans un fichier nomé data_pret1.jsonl"""

def extract_and_replace_asin(page,outfile): # fonction qui permet de scraper les codes(ASIN) identifiant unique de chaque produit sur Amazon 
    
    new_assin=[]
    try :  # recup de ce que le fichier contenait déjà pour éviter qu'un code soit deux fois dans le fichier
        with open(outfile, 'r', encoding='utf-8') as file:
           for line in file:
               new_assin.append(line.strip())
    except:
         print('non réussi')
    try:
        asins = []
        
        # recuperation des produits via le scapping à l'aide d'une api fourni par scrapapi

        payload = { 'api_key': '02ccae5b35eede1c1f2eda2518a30cfb', 'query': 'plaque électrique', 'country_code': 'fr', 'tld': 'fr', 'page': page }
        r = requests.get('https://api.scraperapi.com/structured/amazon/search', params=payload)
        r=r.json()
        product_liste=r['results']
      
        for i in product_liste:
          asins.append(i['asin'])

        print("ASIN extraits :", asins)  # Vérification des ASIN extraits

        if not asins:
            print("Aucun ASIN trouvé ! Vérifiez la structure du fichier.")

        # Écrire uniquement les ASIN dans le fichier (écrase le contenu précédent)
        with open("data.txt", 'a', encoding='utf-8') as file:
            for asin in asins:
                if asin not in new_assin:
                  file.write(asin + "\n")
                else:
                    print('assin existe')

        print("Fichier mis à jour avec succès !")
    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
outfile="data.txt"

#for i in range(5):
  #extract_and_replace_asin(i+1, outfile) 

        
# enregisrement des données prêts dans le fichier data_pret1.json
with open("data14.jsonl", 'r', encoding='utf-8') as file:
            liste_produit=[]
            for line in file:
                produit_copie=produit.copy()
                data = json.loads(line.strip())  # Charger chaque ligne comme un objet JSON
                if "result" in data:
                    asin=data['input']
                    data=data['result']
                    r=json.loads(data)
                    produit_copie['Nom'] = r['name']
                    produit_copie['description'] = r['product_information']
                    produit_copie['image'] = r['images'][0]
                    produit_copie['categorie'] = 'plaque électrique'
                    produit_copie['note'] = r['product_information'].get('moyenne_des_commentaires_client', "0")[0:3]
    
                    if r.get('pricing'):
                       produit_copie['Prix'] = r['pricing']
                       produit_copie['url'] = "https://www.amazon.fr/gp/aw/d/" + asin
                       produit_copie['isan'] = asin

                    if all([r.get('pricing'), r.get('product_information'), r.get('images'), r.get('name')]):
                       liste_produit.append(produit_copie)
    
try:
    with open("data_pret1.jsonl", 'a', encoding='utf-8') as file:
        for i in range(99):
            prod=liste_produit[i]
            prod['indice_ecolo']=calcul_ecolo(prod)
            try:
                ligne_json = json.dumps(prod, ensure_ascii=False)
                file.write(ligne_json + '\n')
                print('ligne ajouté avec succès')
            except (TypeError, ValueError) as e:
                print(f"Erreur de sérialisation pour le produit {prod}: {str(e)}")
                continue
except IOError as e:
    print(f"Erreur d'écriture fichier: {str(e)}")

