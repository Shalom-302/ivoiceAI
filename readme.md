
## **README.md**

```markdown
# Extraction de factures avec Gemini Vision

Cette application Streamlit utilise l'API Google Gemini pour extraire des informations à partir d'images de factures. Elle est déployée sur Streamlit Cloud et peut être utilisée pour automatiser l'extraction de données structurées à partir de documents.

## Fonctionnalités
- Téléchargement d'une image de facture (JPG, JPEG, PNG).
- Extraction des informations suivantes :
  - Titre
  - Entreprise
  - Compte
  - Semaine
  - Total
  - Responsables
- Affichage des informations extraites directement dans l'interface.

## Prérequis
- Un compte Google Cloud avec l'API Gemini activée.
- Une clé API Google valide.

## Installation locale

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/Shalom-302/ivoiceAI.git
   cd votre-depot
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API Google :
   ```env
   GOOGLE_API_KEY=votre_clé_api_ici
   ```

5. Lancez l'application Streamlit :
   ```bash
   streamlit run app.py
   ```

## Déploiement sur Streamlit Cloud

1. Assurez-vous que votre dépôt GitHub est bien configuré et contient les fichiers suivants :
   - `app.py` (votre script Streamlit)
   - `requirements.txt` (liste des dépendances)
   - `.env` (fichier contenant votre clé API)

2. Allez sur [Streamlit Cloud](https://streamlit.io/cloud) et connectez-vous avec votre compte GitHub.

3. Cliquez sur "New App" et sélectionnez votre dépôt GitHub.

4. Configurez les paramètres suivants :
   - **Repository** : Sélectionnez votre dépôt.
   - **Branch** : Sélectionnez la branche principale (généralement `main` ou `master`).
   - **Main file path** : Entrez `app.py`.

5. Ajoutez la clé API Google comme variable d'environnement :
   - Dans la section "Advanced settings", ajoutez une variable d'environnement nommée `GOOGLE_API_KEY` avec votre clé API.

6. Cliquez sur "Deploy" pour lancer le déploiement.

## Structure du projet
```
votre-depot/
├── .env
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Fichier `.gitignore`
Assurez-vous d'ignorer le fichier `.env` pour ne pas exposer votre clé API. Exemple de `.gitignore` :
```
.env
venv/
__pycache__/
```

## Contribution
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, ouvrez une issue ou soumettez une pull request.

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
```

---

## **Fichiers nécessaires pour GitHub**

### 1. **`main.py`**
C'est votre script Streamlit. Assurez-vous qu'il est bien structuré et fonctionnel.

### 2. **`requirements.txt`**
Listez toutes les dépendances nécessaires pour votre projet. Par exemple :
```
streamlit
google-generativeai
python-dotenv
Pillow
```

### 3. **`.env`**
Ce fichier contient votre clé API. **Ne le versionnez pas** (ajoutez-le à `.gitignore`).

### 4. **`.gitignore`**
Ajoutez les fichiers et dossiers à ignorer, comme `.env` et `venv/` :
```
.env
venv/
__pycache__/
```

### 5. **`LICENSE`** (optionnel)
Ajoutez une licence pour votre projet. Par exemple, une licence MIT :
```text
MIT License

Copyright (c) 2024 Shalom Tehe

Permission is hereby granted...
```
