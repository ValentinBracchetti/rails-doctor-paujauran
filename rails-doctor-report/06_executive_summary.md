# 🏥 Audit de Santé — pjr-rails

**Date** : 18 mars 2025
**Réalisé par** : Rails Doctor

---

## Score de santé : 42 / 100

```
🔒 Sécurité       ████░░░░░░  8/30
🧹 Qualité        ██████░░░░  12/20
⚡ Performance    █████░░░░░  10/20
🏗️ Architecture   ████░░░░░░  9/20
📦 Dépendances    ███░░░░░░░  3/10
```

---

## Ce que ça veut dire

Votre application fonctionne, mais elle accumule des risques de sécurité et des freins techniques qui coûteront plus cher à corriger demain. Sans intervention, les coûts de maintenance et le risque d'incidents augmenteront sensiblement. Une action rapide sur les points critiques est recommandée.

---

## Les 5 risques principaux

### 1. Vulnérabilité critique dans GraphQL (exécution de code à distance)

Une faille de sécurité connue dans la bibliothèque GraphQL permet à un attaquant de prendre le contrôle du serveur. La correction est simple (mise à jour) et urgente.

### 2. Données non chiffrées en production

Le chiffrement SSL (HTTPS) est désactivé. Les mots de passe, tokens et données sensibles peuvent être interceptés lors de leur transmission.

### 3. Plus de 40 vulnérabilités dans les bibliothèques

Les composants logiciels (Rails, ActiveAdmin, Puma, etc.) contiennent des failles de sécurité connues. Votre application n'est plus couverte par les mises à jour de sécurité depuis 2023.

### 4. Absence de tests sur les fonctionnalités critiques

Moins de 10 % du code est couvert par des tests. Chaque mise en production comporte un risque de régression non détectée.

### 5. Performance dégradée sous charge

L'application n'est pas équipée pour détecter les requêtes inefficaces (N+1). Le cache n'est pas configuré en production. Les listes de commandes et clients peuvent devenir lentes avec la croissance des données.

---

## Notre recommandation

Nous recommandons de commencer par le **Lot 1 — Quick Wins** (5 jours) pour un investissement de 2 500€ à 5 000€. Cette première phase corrige les risques les plus critiques : activation du SSL, mise à jour de GraphQL, configuration du cache, détection des problèmes de performance. Elle pose les bases pour les chantiers suivants.

Le **Lot 2 — Chantiers Structurants** (18 jours) sécurise l'application à moyen terme : mise à jour de Rails et des bibliothèques, refonte des parties les plus fragiles, augmentation des tests. L'investissement total recommandé est de 23 jours sur 2 à 3 mois.

---

## Budget indicatif

| Phase | Durée | Budget estimé |
|-------|-------|---------------|
| Corrections urgentes (Lot 1) | 5 jours | 2 500€ — 5 000€ |
| Améliorations structurantes (Lot 2) | 18 jours | 9 000€ — 18 000€ |
| Optimisations complémentaires (Lot 3) | 8 jours | 4 000€ — 8 000€ |

---

## Prochaine étape

Nous vous proposons un échange de 30 minutes pour parcourir ce rapport ensemble et répondre à vos questions. Si vous souhaitez avancer, nous pouvons démarrer le Lot 1 sous 2 semaines.

---

*Ce résumé est accompagné d'un rapport technique détaillé (6 fichiers) disponible dans le dossier rails-doctor-report/.*
