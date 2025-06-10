# 🔐 Système de Surveillance Intelligent avec Arduino Yun et Serveur Python

## 📌 Description

Ce projet met en œuvre un **système de surveillance intelligent** combinant un **capteur de mouvement PIR**, une **carte Arduino Yun**, et un **serveur Python** utilisant **Flask** et **OpenCV**. Lorsqu’un mouvement est détecté, une alerte visuelle (LED) et sonore (buzzer) est déclenchée, une photo et une vidéo sont capturées, puis un e-mail est automatiquement envoyé avec les fichiers joints et un lien vers un flux vidéo en direct.

## 🎯 Objectifs

- Détection de mouvement avec un capteur PIR.
- Capture d’image et de vidéo à l’aide d’une webcam.
- Envoi d’un e-mail avec pièces jointes (photo et vidéo) via SMTP.
- Diffusion en temps réel via un serveur Flask.
- Communication entre Arduino et Python par requête HTTP.

## 🛠️ Technologies utilisées

- **Arduino Yun**
- **Capteur PIR**
- **Python 3**
- **OpenCV**
- **Flask**
- **SMTP (smtplib, MIME)**
- **Threading**
- **HTML / Bootstrap (streaming)**

## 📷 Fonctionnalités principales

- 🚨 Alerte immédiate en cas de détection de mouvement.
- 📸 Capture automatique d’une photo.
- 🎥 Enregistrement d’une vidéo de 5 secondes.
- ✉️ Envoi d’un e-mail avec photo + vidéo + lien vers le live stream.
- 🌐 Interface web de streaming local.

## 📽️ Démonstration

- 📸 Capture automatique d'image
- 🎥 Enregistrement vidéo de 5 secondes
- 📧 Envoi d'e-mail avec fichiers en pièce jointe
- 🔴 Streaming en temps réel via webcam
---

## 🧰 Installation

### 1. Prérequis

- Python 3.7+
- Arduino Yun
- Webcam connectée
- Connexion Internet (pour l’envoi d’e-mails)

### 2. Cloner le dépôt

```bash
git clone https://github.com/momonaim/mst-rsi-pfa-motion-alert-system
cd mst-rsi-pfa-motion-alert-system
```

### 3. Installer les dépendances Python

```bash
pip install opencv-python flask python-dotenv
```

### 4. Configuration de l’environnement

Copiez le fichier `.env.example` en `.env`, puis modifiez les valeurs avec vos identifiants :

```bash
cp .env.example .env
```
Ouvrez .env et renseignez :
```bash
EMAIL_SENDER = "votre.email@gmail.com"
EMAIL_PASSWORD = "votre_mot_de_passe"
EMAIL_RECEIVER = "destinataire@email.com"
```

ℹ️ Pour Gmail, utilisez un mot de passe d'application si l'authentification à deux facteurs est activée.


### 5. Lancer le serveur Flask

#### 🔹 Méthode 1 : exécution directe
```bash
python app.py
```
#### 🔹 Méthode 2 : avec la commande flask run
- Sur Linux/macOS :
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```
- Sur Windows :
```bash
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```
🔗 Le serveur sera accessible sur le réseau local à :
`http://<adresse_ip_locale>:5000`
(exemple : http://192.168.1.42:5000/)

### ⚙️ Exemple de déclenchement

Le point d’alerte appelé par Arduino Yun :  
🔗 [http://192.168.1.42:5000/alert](http://192.168.1.42:5000/alert)

Le script Python :

- Capture une photo.

- Enregistre une vidéo.

- Envoie l’e-mail.

- Rend le flux accessible à : /stream.

---



## 📚 Structure du projet

```bash
.
├── app.py # Serveur Flask + logique caméra + alerte
├── photo_lowres.jpg # Image temporaire
├── clip.mp4 # Vidéo enregistrée
├── templates/
│ └── stream.html # Interface de streaming
└── README.md # Ce fichier
```
--- 
## 📄 Licence

Ce projet est à usage académique. Vous pouvez l’adapter ou le partager à des fins éducatives.

---
### Realisé par:

- MOUADILI Abdelmounim


