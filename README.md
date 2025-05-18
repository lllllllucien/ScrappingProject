# 📊 SolanaScrapper Dashboard

Un projet complet pour **scraper les données de prix SOLANA**, les stocker, et les afficher dans un **dashboard web interactif** hébergé sur AWS EC2. Le scraping se fait automatiquement toutes les 5 minutes via un `cron`.

---

## 🚀 Fonctionnalités

 ⏱ Scraping automatique toutes les 5 minutes
 💾 Stockage des données dans un fichier `data.csv`
 📊 Dashboard web avec graphique et rapport latéral
 ☁️ Déploiement facile sur une instance AWS EC2
 🔁 Mise à jour en temps réel via Dash + crontab

---

## 🗂️ Structure du projet

ScrappingProject/
├── Scraping.py # 🔧 Scrape les données SOLANA à partir de fichiers .sh  
├── run.sh # 🕒 Exécute Scraping.py automatiquement via cron  
├── data.csv # 💽 Fichier CSV contenant l'historique des données  
├── Report.py # 📋 Fournit un dictionnaire de métriques via get_report()  
├── Dashboard.py # 🌐 Dashboard Dash (graphiques + panneau latéral)  
├── cron.log # 📄 Log des exécutions cron  
├── dashboard.log # 📄 Log du dashboard lancé avec nohup  
└── README.md # 📘 Fichier d'information du projet  


---

## 🧰 Description des fichiers

- `Scraping.py`  
  → Lit et exécute les scripts `.sh` pour obtenir les données SOLANA depuis des APIs, structure ces données, et met à jour le fichier `data.csv`.

- `run.sh`  
  → Petit script shell lancé par `crontab` toutes les 5 minutes. Il appelle `Scraping.py`.

- `Report.py`  
  → Contient la fonction `get_report()` qui retourne un dictionnaire formaté pour affichage dans le dashboard.

- `Dashboard.py`  
  → Application Dash qui lit `data.csv` et `get_report()` pour afficher un graphe interactif et un panneau de rapport actualisé automatiquement.

- `data.csv`  
  → Fichier de stockage des données SOLANA (timestamp, open, high, low, last price, volume).
  → Ignoré par le gitignore par soucié future de taille de fichier.

- `cron.log`  
  → Fichier qui stocke les sorties du cron (scraping automatique).

- `dashboard.log`  
  → Fichier qui stocke les logs de l’application Dash (via `nohup`).

---

## ⚙️ Installation

### 1. Cloner le dépôt

git clone https://github.com/lllllllucien/ScrappingProject.git  
cd ScrappingProject  


⏱ Automatisation avec cron  
1. Éditer la crontab  

crontab -e  
Et ajouter :  

*/5 * * * * /home/ubuntu/ScrappingProject/run.sh >> /home/ubuntu/ScrappingProject/cron.log 2>&1  

2. Contenu du fichier run.sh  
cd /home/ubuntu/ScrappingProject  
/usr/bin/python3 Scraping.py  

3. Rendre le fichier exécutable  
chmod +x run.sh  

🌐 Lancer le dashboard    
1. Lancer le serveur Dash en arrière-plan    
cd /home/ubuntu/ScrappingProject  
nohup python3 Dashboard.py > dashboard.log 2>&1 &  

2. Accéder au dashboard     
Depuis un navigateur :  
http://16.171.134.172:8050/  

✅ Assure-toi d’avoir ouvert le port 8050 dans le groupe de sécurité AWS EC2.  

🛠 Commandes utiles  

🔍 Vérifier les logs du scraping :  
tail -f cron.log  

🔍 Vérifier les logs du dashboard :  
tail -f dashboard.log  

❌ Stopper le dashboard :  
pkill -f Dashboard.py  

✅ Tester manuellement le scraping :  
python3 Scraping.py  

📌 Auteur  
Projet développé par Sévane Bastian et Lucien Bedel dans le cadre d'un projet scolaire.  

📄 Licence  
Ce projet est libre d'utilisation pour des fins personnelles, éducatives ou non commerciales. Contributions bienvenues !  
