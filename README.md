# 📚 MediaLibrary - Application de gestion de médiathèque

Projet Django permettant la gestion d’une médiathèque numérique avec rôles membre et bibliothécaire.

---

## 🎯 Objectifs du projet

- ✅ Étude et correction du code existant.
- ✅ Implémentation des fonctionnalités demandées.
- ✅ Mise en place d’une stratégie de tests.
- ✅ Fourniture d’une base de données avec données de test.
- ✅ Déploiement sans dépendance externe.

---

## 🛠️ Fonctionnalités

- Authentification des utilisateurs.
- Tableau de bord bibliothécaire (ajout/modification de membres, médias, prêts).
- Interface membre (consultation des médias).
- Système de logs pour traçabilité des actions.
- Templates HTML structurés (admin, prêts, membres, médias).

---

## 🧪 Tests

- Fichier `tests.py` avec tests de base.
- Logs d'accès et d'erreurs pour le suivi comportemental.
- Test à lancer manuellement avec la commande "python manage.py test".

---

## 🗃️ Base de données de test

Le fichier `db.sqlite3` contient :
- Des **utilisateurs préconfigurés**
- Des **médias ajoutés**
- Des **prêts actifs et passés**

> ⚠️ Pour réinitialiser : supprimer `db.sqlite3` et relancer les migrations

---

## 🚀 Installation rapide (aucun prérequis système)

### 1. Cloner le projet ou extraire le `.zip`

```bash
cd medialibrary

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt

---

## Lancer le serveur de développement

python manage.py runserver
Puis aller sur : http://127.0.0.1:8000

---

👥 Comptes de test : 

| Rôle           | Identifiant | Mot de passe          |
| -------------- | ----------- | --------------------- |
| Bibliothécaire | Nico        | Test0303*             |
| Membre         | charlotte   | Test0202*             |

---

📂 Structure du projet

medialibrary/
├── manage.py
├── db.sqlite3
├── medialibrary/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── medialibrary_project/
│   └── settings.py
└── requirements.txt

---

📝 Notes : 

Les journaux (.log) sont générés automatiquement à l'exécution.
Aucune configuration complexe (Docker, PostgreSQL, etc.) n’est nécessaire.

---

🧑‍💻 Auteurs
Projet réalisé par Nicolas.