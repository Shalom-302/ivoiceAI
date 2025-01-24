import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("La clé API Google n'a pas été trouvée dans le fichier .env.")
    st.stop()

genai.configure(api_key=api_key)

st.title("Extraction de factures avec Gemini Vision")

# Ajout du sélecteur de format de sortie
output_format = st.radio(
    "Format de sortie :",
    options=["JSON", "Texte brut"],
    index=0
)

uploaded_file = st.file_uploader("Téléchargez une image de facture", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image téléchargée', use_container_width=True)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Définition dynamique du prompt selon le format
    if output_format == "JSON":
        format_instructions = """
**Format de Sortie:**
Fournis la réponse en format JSON valide avec la structure suivante :
{
    "en_tete": {
        "titre": "string",
        "entreprise": "string",
        "date": "string",
        "client": "string",
        "semaine": "string",
        "operation": "string",
        "produit": "string",
        "site": "string"
    },
    "tableau": [
        {
            "numero": "int",
            "identifiant": "string",
            "description": "string",
            "valeur": "float",
            "observation": "string"
        }
    ],
    "total": "float",
    "pied_de_page": {
        "entreprises": ["string"],
        "magasinier": {
            "nom": "string",
            "date": "string"
        },
        "autres_signataires": [
            {
                "nom": "string",
                "role": "string"
            }
        ]
    }
}
"""
    else:
        format_instructions = """
**Format de Sortie:**
Fournis la réponse dans un format texte structuré avec :
- Des sections clairement identifiées (En-tête, Tableau, Total, Pied de page)
- Des tableaux formatés en Markdown
- Des listes d'informations organisées

Exemple de structure :
**En-tête:**
- Titre: ...
- Entreprise: ...
- Date: ...
...

**Tableau:**
| N° | Identifiant | Description | Valeur | Observation |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

**Total:** ...

**Pied de page:**
- Entreprises: [...]
- Magasinier: ...
...
"""

    prompt = f"""
Analyse l'image d'un document de type "{{document_type}}". Ce document est une sorte de récapitulatif journalier.

**Structure du document:**
Le document contient généralement :
- Un en-tête avec des informations générales
- Un tableau de données structurées
- Un total global
- Un pied de page avec signatures

**Instructions d'extraction:**
1. En-tête:
   - Extrait toutes les métadonnées visibles
   - Identifie les éléments contextuels importants

2. Tableau:
   - Repère toutes les lignes et colonnes
   - Conserve l'ordre original des données
   - Corrige les symboles incomplets

3. Total:
   - Localise et vérifie le calcul

4. Pied de page:
   - Identifie toutes les entités responsables
   - Extrait les détails des signatures

{format_instructions}

**Consignes importantes:**
- Sois précis et exhaustif
- Conserve la structure originale
- Ne modifie pas les valeurs
- Signale les éléments ambigus
"""

    response = model.generate_content([prompt, image])
    
    st.subheader("Résultat de l'analyse")
    
    if output_format == "JSON":
        try:
            # Tentative de formatage pour une meilleure lisibilité
            json_data = eval(response.text)
            st.json(json_data)
        except:
            st.write(response.text)
    else:
        st.markdown(response.text)