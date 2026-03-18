# 📋 Plan d'Action Priorisé

**Date** : 18 mars 2025
**Projet** : pjr-rails
**Score santé global** : 42 / 100

---

## Vue d'ensemble

| Domaine | Score | Critiques | Majeurs | Mineurs |
|---------|-------|-----------|---------|---------|
| 🔒 Sécurité | 8/30 | 4 | 6 | 2 |
| 🧹 Qualité | 12/20 | 2 | 5 | 5 |
| ⚡ Performance | 10/20 | 1 | 4 | 3 |
| 🏗️ Architecture | 9/20 | 2 | 4 | 4 |
| 📦 Dépendances | 3/10 | 1 | 1 | 0 |
| **Total** | **42/100** | **10** | **20** | **14** |

---

## 🟢 Lot 1 — Quick Wins

**Estimation totale** : 5 jours
**Impact** : Correction immédiate des risques les plus critiques avec un effort minimal.
**Vendabilité** : ⭐⭐⭐

Ces améliorations peuvent être livrées rapidement et leur valeur est immédiatement visible.

| # | Finding | Domaine | Sévérité | Effort | Impact |
|---|---------|---------|----------|--------|--------|
| 1 | SEC-002 — Activer force_ssl | Sécurité | 🔴 | XS | Conformité SSL |
| 2 | SEC-005 — Réduire log_level en production | Sécurité | 🟠 | XS | Réduction fuites |
| 3 | SEC-006 — Configurer CORS correctement | Sécurité | 🟠 | XS | Sécurité API |
| 4 | SEC-008 — Externaliser secrets dev/test | Sécurité | 🟠 | XS | Secrets sécurisés |
| 5 | SEC-001 — Mise à jour graphql (CVE RCE) | Sécurité | 🔴 | S | Élimination CVE critique |
| 6 | PERF-001 — Ajouter Bullet | Performance | 🔴 | XS | Détection N+1 |
| 7 | PERF-003 — Configurer cache_store | Performance | 🟠 | S | Cache production |
| 8 | PERF-005 — Précharger associations QueryType | Performance | 🟠 | XS | Moins de requêtes |
| 9 | CQ-005 — Mémoïser Rails.logger/Time.zone (jobs) | Qualité | 🟠 | XS | Code propre |
| 10 | CQ-007 — Use scope access UsersController | Qualité | 🟠 | XS | Réutilisation |

### Détail des actions

#### SEC-002 — Activer force_ssl
- **Action** : Décommenter `config.force_ssl = true` dans `config/environments/production.rb`
- **Livrable** : SSL forcé, redirection HTTP → HTTPS
- **Estimation** : 30 min

#### SEC-005 — Réduire log_level en production
- **Action** : Remplacer `config.log_level = :debug` par `:info` (ou `:warn`)
- **Livrable** : Logs moins verbeux en production
- **Estimation** : 15 min

#### SEC-006 — Configurer CORS correctement
- **Action** : Remplacer `origins 'example.com'` par les domaines réels via ENV
- **Livrable** : CORS configuré pour le frontend réel
- **Estimation** : 1 h

#### SEC-008 — Externaliser secrets dev/test
- **Action** : Utiliser ENV ou credentials pour secret_key_base en dev/test
- **Livrable** : Aucun secret en clair dans secrets.yml
- **Estimation** : 1 h

#### SEC-001 — Mise à jour graphql (CVE RCE)
- **Action** : `bundle update graphql` vers >= 2.0.32
- **Livrable** : CVE-2025-27407 corrigée
- **Estimation** : 2-4 h (tests de non-régression)

#### PERF-001 — Ajouter Bullet
- **Action** : Ajouter gem bullet, configurer en development
- **Livrable** : Alertes N+1 en dev
- **Estimation** : 1 h

#### PERF-003 — Configurer cache_store
- **Action** : Configurer :mem_cache_store ou :redis_cache_store en production
- **Livrable** : Cache partagé fonctionnel
- **Estimation** : 2-4 h

#### PERF-005 — Précharger associations QueryType
- **Action** : Ajouter includes dans all_clients et client selon les champs
- **Livrable** : Moins de requêtes sur les listes clients
- **Estimation** : 2 h

#### CQ-005 — Mémoïser Rails.logger/Time.zone (jobs)
- **Action** : `today = Time.zone.today` et `logger = Rails.logger` en début de perform
- **Livrable** : Code plus propre
- **Estimation** : 1 h

#### CQ-007 — Use scope access UsersController
- **Action** : Créer un scope User et l'utiliser dans le controller
- **Livrable** : Logique de requête centralisée
- **Estimation** : 1 h

---

## 🟡 Lot 2 — Chantiers Structurants

**Estimation totale** : 18 jours
**Impact** : Amélioration profonde de la sécurité, performance et maintenabilité.
**Vendabilité** : ⭐⭐

Ces chantiers nécessitent un investissement plus important mais sécurisent l'application à moyen terme.

| # | Finding | Domaine | Sévérité | Effort | Impact |
|---|---------|---------|----------|--------|--------|
| 1 | SEC-003 — Mise à jour ActiveAdmin | Sécurité | 🔴 | M | XSS, CSV injection |
| 2 | SEC-004 — Migration Rails 6.0 → 6.1+ | Sécurité | 🔴 | S-M | SQL injection, EOL |
| 3 | SEC-007 — Mise en place CSP | Sécurité | 🟠 | S | Défense XSS |
| 4 | SEC-009+ — Mise à jour dépendances (CVEs) | Sécurité | 🟠 | L | 40+ CVEs |
| 5 | CQ-001 — Refactorer UpdateClient | Qualité | 🔴 | M | Maintenabilité |
| 6 | CQ-002 — Corriger Law of Demeter mapotempo | Qualité | 🔴 | S | Découplage |
| 7 | CQ-003 — Supprimer méthodes inutilisées | Qualité | 🟠 | S | Code mort |
| 8 | CQ-004 — Refactorer mutations Order | Qualité | 🟠 | S | Duplication |
| 9 | CQ-006 — Extraire logique Import/Invoice | Qualité | 🟠 | S | Services |
| 10 | PERF-002 — Résoudre N+1 GraphQL | Performance | 🟠 | S | Requêtes |
| 11 | PERF-004 — Fragment caching | Performance | 🟠 | M | Charge serveur |
| 12 | ARCH-001 — Enrichir couche Service | Architecture | 🔴 | M | Réutilisation |
| 13 | ARCH-002 — Augmenter couverture tests | Architecture | 🔴 | L | Confiance |
| 14 | ARCH-003 — Form Objects, Policies | Architecture | 🟠 | L | Structure |
| 15 | ARCH-004 — Migration Rails | Architecture | 🟠 | M | Support |
| 16 | ARCH-005 — Dépendances obsolètes | Architecture | 🟠 | S | Stack moderne |

### Détail des actions

#### SEC-003 — Mise à jour ActiveAdmin
- **Action** : Mettre à jour vers ActiveAdmin >= 3.2.2 (ou 4.x)
- **Livrable** : CVE XSS et CSV injection corrigées
- **Estimation** : 1-3 j (breaking changes possibles)
- **Prérequis** : Tests de non-régression admin

#### SEC-004 — Migration Rails 6.0 → 6.1+
- **Action** : Mise à jour Gemfile, résolution des dépréciations, tests
- **Livrable** : Rails supporté, CVE ActiveRecord corrigées
- **Estimation** : 1-2 j
- **Prérequis** : Environnement de staging

#### SEC-007 — Mise en place CSP
- **Action** : Créer config/initializers/content_security_policy.rb
- **Livrable** : Headers CSP envoyés
- **Estimation** : 2-4 h
- **Prérequis** : Aucun

#### SEC-009+ — Mise à jour dépendances
- **Action** : bundle update sur les gems vulnérables (puma, loofah, rexml, etc.)
- **Livrable** : Réduction des CVEs
- **Estimation** : 3-5 j (tests, résolution de conflits)
- **Prérequis** : Migration Rails (certaines gems dépendent de la version Rails)

#### CQ-001 — Refactorer UpdateClient
- **Action** : Introduire ClientAttributesInput, grouper les assignations
- **Livrable** : Mutation lisible, maintenable
- **Estimation** : 1-2 j
- **Prérequis** : Tests sur la mutation

#### CQ-002 — Corriger Law of Demeter mapotempo
- **Action** : Introduire méthodes déléguées ou Presenter
- **Livrable** : Découplage mapotempo
- **Estimation** : 4-8 h
- **Prérequis** : Aucun

#### PERF-002 — Résoudre N+1 GraphQL
- **Action** : graphql-batch ou DataLoader, ou includes dans résolveurs
- **Livrable** : Requêtes GraphQL optimisées
- **Estimation** : 4-8 h
- **Prérequis** : Bullet pour valider

#### ARCH-001 — Enrichir couche Service
- **Action** : Créer ImportService, InvoiceCreationService, OrderValidationService
- **Livrable** : Logique métier extraite des models
- **Estimation** : 2-3 j
- **Prérequis** : Tests sur les chemins critiques

#### ARCH-002 — Augmenter couverture tests
- **Action** : Specs pour mutations GraphQL, services, jobs
- **Livrable** : Ratio spec/code ≥ 0.3
- **Estimation** : 5-10 j
- **Prérequis** : Aucun

---

## 🔵 Lot 3 — Nice to Have

**Estimation totale** : 8 jours
**Impact** : Amélioration de la qualité de vie des développeurs et maintenabilité long terme.
**Vendabilité** : ⭐

| # | Finding | Domaine | Sévérité | Effort | Impact |
|---|---------|---------|----------|--------|--------|
| 1 | CQ-009 — Noms de variables | Qualité | 🟡 | M | Lisibilité |
| 2 | CQ-010 — Documentation (IrresponsibleModule) | Qualité | 🔵 | L | Onboarding |
| 3 | CQ-012 — DataClump ProductionOrder | Qualité | 🔵 | S | Value Object |
| 4 | PERF-006 — Index manquants | Performance | 🟡 | S | Requêtes |
| 5 | ARCH-006 — Réviser callbacks | Architecture | 🟠 | S | Testabilité |
| 6 | ARCH-008 — GraphQL versioning | Architecture | 🟡 | M | Évolution API |
| 7 | ARCH-010 — Monitoring applicatif | Architecture | 🟡 | S | Observabilité |

---

## Estimation budgétaire

| Lot | Jours estimés | Fourchette budgétaire* |
|-----|---------------|-------------------------|
| Quick Wins | 5 j | 2 500€ — 5 000€ |
| Chantiers Structurants | 18 j | 9 000€ — 18 000€ |
| Nice to Have | 8 j | 4 000€ — 8 000€ |
| **Total** | **31 j** | **15 500€ — 31 000€** |

*Fourchette indicative basée sur un TJM de 500€ à 1 000€.
Les estimations seront affinées lors du cadrage détaillé de chaque lot.

---

## Recommandation de séquencement

```
Mois 1          Mois 2-3              Mois 4+
┌──────────┐    ┌──────────────┐      ┌──────────────┐
│ LOT 1    │───▶│ LOT 2        │─────▶│ LOT 3        │
│ Quick    │    │ Structurant  │      │ Nice to Have │
│ Wins     │    │              │      │              │
└──────────┘    └──────────────┘      └──────────────┘
```

**Approche recommandée** : livraison itérative par sprints de 2 semaines, avec une revue de progression à chaque fin de sprint.
