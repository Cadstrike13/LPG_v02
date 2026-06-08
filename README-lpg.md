# Les Penseurs du Gabon — Site Web + API Django

## Architecture

```
lpg-site/
├── django_api/
│   └── lpg/
│       ├── models.py      ← Modèles de données
│       ├── views.py       ← Endpoints API (mock → DB en prod)
│       └── urls.py        ← Routing API
└── frontend/
    └── lpg-site.html      ← Site complet (HTML/CSS/JS)
```

---

## Installation Django

```bash
pip install django djangorestframework django-cors-headers

django-admin startproject lpg_project
cd lpg_project
python manage.py startapp lpg
```

**settings.py** — ajouter :
```python
INSTALLED_APPS += [
    "corsheaders",
    "lpg",
]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
CORS_ALLOW_ALL_ORIGINS = True  # restreindre en prod
```

**urls.py (projet)** :
```python
from django.urls import path, include
urlpatterns = [
    path("", include("lpg.urls")),
]
```

---

## Endpoints API

| Méthode | URL                     | Description                     |
|---------|-------------------------|---------------------------------|
| GET     | `/api/all/`             | Tout le contenu en un seul appel ✅ |
| GET     | `/api/config/`          | Config générale (nom, logo…)    |
| GET     | `/api/about/`           | Texte Mission/Vision            |
| GET     | `/api/values/`          | Valeurs (grille 2×2)            |
| GET     | `/api/objectives/`      | 4 objectifs fondamentaux        |
| GET     | `/api/actions/`         | 6 actions principales           |
| GET     | `/api/board-roles/`     | Rôles du Conseil d'Admin        |
| GET     | `/api/member-types/`    | Types de membres                |
| GET     | `/api/membership-plans/`| Plans d'adhésion + tarifs       |
| GET     | `/api/contact/`         | Coordonnées                     |
| GET     | `/api/join-statements/` | Messages "Rejoignez-nous"       |

---

## Connecter le frontend au backend

Dans `lpg-site.html`, ligne ~290 :

```js
// Actuellement (mode démo sans backend) :
const API_BASE = window.LPG_API_BASE || null;

// Pour pointer vers votre Django local :
const API_BASE = "http://localhost:8000";

// OU injecter depuis Django (template) :
// <script>window.LPG_API_BASE = "{{ request.scheme }}://{{ request.get_host }}";</script>
```

---

## Lancer en développement

```bash
python manage.py runserver
# → http://localhost:8000/api/all/
```

Ouvrir `lpg-site.html` dans le navigateur — les données se chargent depuis l'API.

---

## Données modifiables

Tout le contenu du site est modifiable via l'API Django :

| Donnée                  | Fichier à éditer        | Variable mock           |
|-------------------------|-------------------------|-------------------------|
| Nom, logo, devise       | `views.py` → `MOCK_CONFIG`       | `config`     |
| Texte Mission/Vision    | `views.py` → `MOCK_ABOUT`        | `about`      |
| Valeurs (4 cartes)      | `views.py` → `MOCK_VALUES`       | `values`     |
| Objectifs (4 blocs)     | `views.py` → `MOCK_OBJECTIVES`   | `objectives` |
| Actions (6 cartes)      | `views.py` → `MOCK_ACTIONS`      | `actions`    |
| Rôles du bureau         | `views.py` → `MOCK_BOARD_ROLES`  | `board_roles`|
| Types de membres        | `views.py` → `MOCK_MEMBER_TYPES` | `member_types`|
| Plans & tarifs          | `views.py` → `MOCK_MEMBERSHIP_PLANS` | `membership_plans`|
| Coordonnées             | `views.py` → `MOCK_CONTACT`      | `contact`    |
| Messages rejoindre      | `views.py` → `MOCK_JOIN_STATEMENTS` | `join_statements`|

---

## Palette de couleurs

| Nom           | Hex       | Usage                          |
|---------------|-----------|--------------------------------|
| Brun profond  | `#2B0F00` | Fond navbar, entêtes sections  |
| Brun principal| `#3D1A00` | Fond hero et sections brunes   |
| Brun carte    | `#4A2000` | Cartes objectifs, plans dark   |
| Or/Gold       | `#C8A200` | Titres, accents, surlignes     |
| Or clair      | `#E0B800` | Titres hero principaux         |
| Crème         | `#F0EAD6` | Fond sections claires          |
| Vert Gabon    | `#009A00` | CTA bouton, stripe drapeau     |
| Jaune Gabon   | `#FFD100` | Stripe drapeau                 |
| Bleu Gabon    | `#003F87` | Stripe drapeau                 |
