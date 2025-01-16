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
    st.image(image, caption='Image téléchargée', use_column_width=True)
    
    # Initialiser le modèle Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Définir le prompt
    prompt = """
    Extrais les informations suivantes de cette facture :
    - Titre
    - Entreprise
    - Compte
    - Semaine
    - Total
    - Responsables
    """
    
    # Envoyer l'image et le prompt au modèle
    response = model.generate_content([prompt, image])
    
    # Afficher la réponse
    st.subheader("Informations extraites :")
    st.write(response.text)