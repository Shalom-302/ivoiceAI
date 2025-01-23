import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()  # Assurez-vous que le fichier .env est dans le même répertoire

# Récupérer la clé API
api_key = os.getenv("GOOGLE_API_KEY")

# Vérifier si la clé API est chargée
if not api_key:
    st.error("La clé API Google n'a pas été trouvée dans le fichier .env.")
    st.stop()

# Configurer l'API Gemini
genai.configure(api_key=api_key)

# Interface Streamlit
st.title("Extraction de factures avec Gemini Vision")

# Upload de l'image
uploaded_file = st.file_uploader("Téléchargez une image de facture", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Ouvrir l'image
    image = Image.open(uploaded_file)
    
    # Afficher l'image
    st.image(image, caption='Image téléchargée', use_container_width=True)
    
    # Initialiser le modèle Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Définir le prompt
    prompt = """
   Analyse l'image d'un document de type "{document_type}". Ce document est une sorte de récapitulatif journalier.

**Structure du document:**
Le document contient généralement un en-tête, un tableau de données, un total et un pied de page.
* L'en-tête contient des informations générales sur le document.
* Le tableau contient des données structurées sur des items (ex: camions).
* Le total est une somme des données du tableau.
* Le pied de page contient des informations sur les responsables et leurs signatures.

**Instructions d'extraction:**

1. **En-tête:**
    * Extrais le titre du document.
    * Identifie et extrais le nom de l'entreprise (responsable du document).
    * Extrait la date du document.
    * Extrait le nom du client (si présent).
    * Extrait la semaine concernée (si présente).
    * Identifie l'opération effectuée (si présente).
    * Extrait le nom du produit transporté (si présent).
    * Extrait le site concerné (si présent).

2. **Tableau:**
    * Extrais les données du tableau. Chaque ligne contient:
        * un numéro d'ordre (N°)
        * un identifiant de l'item (ex: un numéro de camion)
        * une description de l'item (ex: type de produit)
        * une valeur (ex: un tonnage)
        * une observation (si présente)
    * Si une entrée de la description de l'item est représentée par un symbole comme "{symbol_replacement}", remplace-le par la description complète trouvée dans l'en-tête ou ailleurs si c'est déductible.

3. **Total:**
    * Extrait la valeur du total.

4. **Pied de page:**
    * Identifie les entreprises (responsable du document et celle du destinataire) pour les signatures.
    * Extrait le nom et la date du signataire du MAGASINIER si existant.
    * Extrait et liste tout autre signataire avec son rôle.

**Format de Sortie:**
Fournis la réponse dans un format texte structuré, de façon claire et lisible, en gardant l'organisation du document original. Utilise un format de tableau pour les données de items, comme dans l'original.

Exemple (incomplet):

**En-tête:**
Titre: {document_title}
Entreprise: {document_enterprise}
...

**Tableau:**
| N° | {item_identifier_label} | {item_description_label} | {item_value_label} | observation |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
...

**Total:**
Total: ...

**Pied de page:**
Entreprise: {responsible_enterprise}
Responsable: ...

Entreprise: {destinataire_enterprise}
Magasinier: ...
Date: ...
Responsable: ...

**Variables à remplacer:**

* `{document_type}`: Le type de document (ex: "récap journalier", "feuille de chargement", etc.).
* `{symbol_replacement}`: Le symbole utilisé pour représenter une valeur manquante ou à remplacer (ex: " ", "–", etc.).
* `{document_title}`: Placeholder pour le titre du document (à adapter en fonction du format).
* `{document_enterprise}`: Placeholder pour le nom de l'entreprise du document.
* `{item_identifier_label}`: Label utilisé pour identifier l'item (ex: "Numéro de camion", "Référence", etc.).
* `{item_description_label}`: Label utilisé pour la description de l'item (ex: "produit", "type", etc.).
* `{item_value_label}`: Label utilisé pour la valeur (ex: "tonnage", "quantité", etc.).
* `{responsible_enterprise}`: Placeholder pour le nom de l'entreprise du responsable.
* `{destinataire_enterprise}`: Placeholder pour le nom de l'entreprise destinataire.

**Comment utiliser ce template:**

1.  **Adaptation:**  Adaptez les placeholders et les instructions en fonction des documents que vous souhaitez analyser. Vous devrez probablement ajuster `{item_identifier_label}`, `{item_description_label}` et `{item_value_label}` selon le contexte du tableau.
2.  **Entrée:** Remplissez les variables et soumettez le prompt au modèle d'IA avec l'image correspondante.
3.  **Extraction:** Le modèle traitera l'image, extraira les informations, puis les présentera dans un format textuel structuré.

**Avantages du template :**

*   **Réutilisable:** Vous pouvez utiliser ce template pour différents documents du même type, en modifiant seulement quelques variables.
*   **Personnalisable:** Vous pouvez ajuster les instructions et les placeholders pour correspondre au mieux à vos besoins.
*   **Clair et structuré:** Il fournit une base solide pour l'extraction de données, en s'assurant que le modèle sait quoi extraire et comment le formater.

    """
    
    # Envoyer l'image et le prompt au modèle
    response = model.generate_content([prompt, image])
    
    # Afficher la réponse
    st.subheader("Informations extraites :")
    st.write(response.text)