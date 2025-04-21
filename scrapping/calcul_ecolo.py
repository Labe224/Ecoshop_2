import requests
import json
from decouple import config   # bibliothèque qui permet de recuperer les variables globales


""" Programme qui nous permet de calculer la note écologie d'un produits """

produit={ # objet qui répresente un produits 
    "Nom":'',
    "Prix":0,
    "categorie":"",
    "image":"",
    "description":{},
    "isan":"",
    "indice_ecolo":0,
    'url':"",
    'note':""
} 




Ecv_de_base={  #Dictionnaire qui donne l'impact carbone d'un produit electromenagers durant sa durée d'utilisation 
                # l'unité est le Kg C02e
  "bouilloire":37.8,
  "aspirateur":73.4,
  "micro onde":121,
  "cafétière filtre": 191,
   "cafétière expresso":212,
   "cafétière dosettes":238,
   "four électrique":273,
   "réfrigérateur":339,
   "climatiseur":422,
   "lave vaisselle":461,
   "lave linge":513,
   "chauffages éctrique":745,
   "chauffages au gaz":2457,
   "chauffages au fiol":3601.71,
   "mixeur":75.65,
   "plaque à induction":235,
   "plaque électrique":265,
   "chauffages avec une pompe à chaleur":248.85
}  # Données obtenue sur ADEME à travers le site impactc02.gouv.fr sauf pour le mixeur et les plaques

# Note a attribué selon le label
note_label={'A':5,'A+++':5,'A++':10,'A+':5,'B':10,'C':15,'D':20,'E':25,'F':30,'G':30} 


#fonction Info_IA qui utilise l'api de openIA pour nous fournir certains informations sur le produits 
api_key_valid=config('API_KEY2') # recuperation de la clé api pour OpenAI
def Info_IA(produit):
    API_KEY = api_key_valid
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"

}

    data = {
    "model": "gpt-4-turbo",  # Version plus récente que gpt-4
    "messages": [
        {
            "role": "system", 
            "content": "Tu es un expert en analyse environnementale de produits. Tu réponds UNIQUEMENT par des valeurs estimées au format JSON strict, sans aucun commentaire."
        },
        {
            "role": "user", 
            "content": f"""Estime les données environnementales du produit suivant en t'appuyant sur tes connaissances techniques. 

Description : {produit['description']}
Image (à titre indicatif) : {produit['image']}

Réponse obligatoire en JSON avec ces champs remplis :
- conso_electrique(kwh) : entier ≥ 0 (estimation kWh/an)
- conso_eau(l) : entier ≥ 0 (estimation litres/an)
- Label_energetique : lettre entre A et G
- indice_reparbitite : entier entre 1 (irréparable) et 10 (très réparable)
- Matériaux : chaîne de caractères
- recyclable : 0 (non) ou 1 (oui)

Si une information est inconnue, donne une estimation plausible."""
        }
    ],
    "temperature": 0.1,  # Plus bas que 0.2 pour maximiser la cohérence
    "response_format": {"type": "json_object"},
    "top_p": 0.3  # Limite les réponses aux options les plus probables
}


    response = requests.post(url, headers=headers, json=data)

    response=response.json()
    

    v=response['choices'][0]['message']['content']
    v_json=json.loads(v)
    return v_json




def calcul_ecolo(produit): # fonction qui permet de calculer l'indice écologique d'un produit données 

    note=0  # la note sera sur 100 le produit le plus écolo est 0 et le moins ecolo est 10
    cat=produit['categorie']
       
    note=Ecv_de_base[cat]/100 #vu les données on obtient un nombre entre 0.73 et 33,1

    note_IA=0  #note obtenu à base de l'IA
    note_nIA=0  #note à base de la description


    # calcul écologique sans IA 

    if 'niveau_sonore' in produit['description']:
      try:
        note_nIA = int(produit['description']['niveau_sonore'][0:3]) / 10
      except:
         note_nIA=0.1

    if 'classe_denergie' in produit['description']:
        l_energie = produit['description']['classe_denergie']

        if l_energie in note_label:  # Vérification que la clé existe dans note_label
            note_nIA += note_label[l_energie]


    if 'efficacite_energetique_10_niveaux' in produit['description']:
        l_energie=produit['description']['efficacite_energetique_10_niveaux']
        if l_energie in note_label:
           note_nIA+=note_label[l_energie]


    if 'certification' in produit['description']:
       note_nIA -= 10
  
    donnees_IA=Info_IA(produit) # recuperation des données fournis par l'IA

    if donnees_IA :
     if donnees_IA["recyclable"]==0:
        note_IA+=10
    
     l_energie=donnees_IA['Label_energetique']
     
     if  l_energie not in note_label:
        l_energie='B'
    
     note_IA+=note_label[l_energie]

     note_IA+=10/donnees_IA['indice_reparbitite']

     
    if note_nIA!=0:
      note=note+0.5*note_IA+note_nIA

    else:
       note=note+0.75*note_IA

    if note>100:
       
       note=100 #produit qui n'est pas du tout écologique

    if 0>note:
       note=1  #produit très écologique

    return note
    

