Je vais créer un backoffice complet — dark theme professionnel, système login + JWT simulé, et gestion de toutes les sections du site LPG.

Voilà le backoffice complet ! Voici ce qui est inclus :

---

## 🔐 Système d'authentification

- Écran de login avec validation
- Session JWT simulée (sessionStorage) — reconnexion automatique si la session est active
- Déconnexion propre
- Changement de mot de passe depuis l'espace Utilisateurs
- **Accès demo : admin / lpg2024**

---

## 📋 Toutes les sections gérables

| Section | Ce qu'on peut faire |
|---|---Config généralele** | Nom, acronyme, slogan, stats, devise, logo, CTA Mission & Visionon** | Titre, 2 paragraphes Valeursrs** | Ajouter / modifier / supprimer (icône + titre + desc) Objectifsfs** | Ajouter / modifier / supprimer (numéro + icône + titre + desc) Actionsns** | Ajouter / modifier / supprimer (6 cartes) Organisationon** | Rôles du bureau + 4 types de membres Adhésion & Tarifsfs** | 2 plans (tarif, avantages, mise en avant) Contactct** | Adresse, emails, téléphones, réseaux sociaux, messages "rejoignez-nous" |

---

## 🔌 Connexion Django

Dans la pAPI & Intégrationon**, il suffit de coller l'URL du serveur Django (ex: http://localhost:8000) et de cliqTester la connexionon** — le bouton ping directement /api/all/.