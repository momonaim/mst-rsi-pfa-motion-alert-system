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

## 🧰 Installation

### 1. Prérequis

- Python 3.7+
- Arduino Yun
- Webcam connectée
- Connexion Internet (pour l’envoi d’e-mails)

### 2. Cloner le dépôt

```bash
git clone https://github.com/votre-nom-utilisateur/nom-du-repo.git
cd nom-du-repo
```

### 3. Installer les dépendances Python

```bash
pip install opencv-python flask
```

### 4. Modifier les identifiants e-mail

Dans le fichier Python :

```bash
EMAIL_SENDER = "votre.email@gmail.com"
EMAIL_PASSWORD = "votre_mot_de_passe"
EMAIL_RECEIVER = "destinataire@email.com"
```

### 5. Lancer le serveur Flask

```bash
python app.py
```

Le serveur tourne sur : http://localhost:5000

### ⚙️ Exemple de déclenchement

L’Arduino envoie une requête à :

http://<ip_serveur>:5000/alert
Le script Python :

- Capture une photo.

- Enregistre une vidéo.

- Envoie l’e-mail.

- Rend le flux accessible à : /stream.

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

## 📄 Licence

Ce projet est à usage académique. Vous pouvez l’adapter ou le partager à des fins éducatives.

### Realisé par:

- MOUADILI Abdelmounim
