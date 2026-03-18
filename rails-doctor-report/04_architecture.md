# 🏗️ Architecture

**Score du domaine** : 9 / 20

---

## Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | 2 |
| 🟠 Majeur | 4 |
| 🟡 Mineur | 4 |
| 🔵 Cosmétique | 0 |

**Outils utilisés** : Analyse manuelle (structure, patterns, dépendances)

---

## Findings

### 🔴 ARCH-001 — Ratio services/models insuffisant (0.11 vs 0.3)

**Sévérité** : Critique | **Effort** : M (1-3j) | **Vendabilité** : ⭐⭐

**Localisation** : `app/services/` (3 services) vs `app/models/` (27 models)

**Constat** :
Le projet compte 3 services (CryptoService, ExpoPushNotificationService, TwilioService) pour 27 models. Ratio 0.11. Un projet sain vise ≥ 0.3. La logique métier complexe (Import, InvoiceGroup, Order validation, DailySubscription) reste dans les models.

**Risque si non corrigé** :
Chaque nouvelle fonctionnalité nécessite de modifier les models existants. Pas de briques réutilisables. Tests difficiles car la logique est couplée aux modèles ActiveRecord.

**Recommandation** :
Extraire progressivement la logique métier vers des services : `ImportService`, `InvoiceCreationService`, `OrderValidationService`, `DailySubscriptionOrderGenerator`. Les models conservent validations et associations ; les services orchestrent les opérations.

**Bénéfice attendu** :
Réutilisation, testabilité, séparation des responsabilités.

---

### 🔴 ARCH-002 — Couverture de tests insuffisante

**Sévérité** : Critique | **Effort** : L (3-10j) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `spec/` — 9 fichiers de test pour ~99 fichiers dans app/

**Constat** :
- 9 specs : 6 models (access_token, client, order, invoice, email_password_authenticable, access_token_authenticable), 2 features (admin, admin/client), 1 graphql (basket)
- Aucun spec pour : UsersController, SessionController, GraphQL mutations (UpdateClient, Order, SignIn, SignUp, etc.), Jobs, Services (Crypto, Expo, Twilio), la majorité des models (Invoice, Subscription, Catalog, etc.)

**Risque si non corrigé** :
Chaque déploiement est un pari. Les régressions ne sont pas détectées. Refactoring risqué. Onboarding lent car le code n'est pas documenté par des tests.

**Recommandation** :
Prioriser les tests sur : mutations GraphQL critiques (UpdateClient, Order, SignIn), services (ExpoPushNotificationService, TwilioService), jobs (DailyCreateOrdersJob, DailyValidateOrdersJob). Viser un ratio spec/code ≥ 0.3.

**Bénéfice attendu** :
Confiance pour déployer et refactorer. Documentation vivante du comportement attendu.

---

### 🟠 ARCH-003 — Patterns manquants : Form Objects, Query Objects, Presenters, Policies

**Sévérité** : Majeur | **Effort** : L (3-10j) | **Vendabilité** : ⭐⭐

**Localisation** : Global

**Constat** :
- **Form Objects** : Mutations GraphQL avec 52 paramètres (UpdateClient) — un Form Object structurerait les inputs
- **Query Objects** : Scopes complexes enchaînés dans QueryType et Admin (ex. `client.orders.not_canceled.for_tag(tag).find_by(...)`) — des Query Objects amélioreraient la lisibilité
- **Presenters/Decorators** : Logique de présentation dans ClientType, OrderType (display_name, image_url) — acceptable pour GraphQL, mais mapotempo.rb mélange logique et présentation
- **Policy Objects** : `ensure_current_user_is_admin!` et `ensure_has_current_user!` dans les types — pas de couche Policy centralisée (Pundit, etc.)

**Risque si non corrigé** :
Logique dispersée. Évolution coûteuse. Autorisation et validation difficiles à auditer.

**Recommandation** :
Introduire des Form Objects pour les mutations complexes. Créer des Query Objects pour les requêtes réutilisables. Envisager Pundit ou une couche Policy pour centraliser l'autorisation.

**Bénéfice attendu** :
Code plus structuré, autorisation centralisée, validations réutilisables.

---

### 🟠 ARCH-004 — Rails 6.0 en fin de vie (EOL)

**Sévérité** : Majeur | **Effort** : M (1-3j) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `Gemfile` — `rails ~> 6.0.1`

**Constat** :
Rails 6.0 a atteint sa fin de support de sécurité en juin 2023. Aucun correctif de sécurité n'est plus fourni pour cette version. Le projet est exposé aux CVEs connues et futures.

**Risque si non corrigé** :
Non-conformité pour les audits sécurité (RGPD, ISO 27001). Assurance et clients peuvent exiger une version supportée.

**Recommandation** :
Planifier une migration vers Rails 6.1 (LTS jusqu'à juin 2024) ou Rails 7.x. Tester en environnement de staging. Mettre à jour les gems dépendantes (ActiveAdmin, Devise, etc.).

**Bénéfice attendu** :
Support sécurité, accès aux nouvelles fonctionnalités Rails.

---

### 🟠 ARCH-005 — Dépendances obsolètes

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `Gemfile`

**Constat** :
- `coffee-rails` — CoffeeScript est en maintenance minimale, la communauté a migré vers ES6/TypeScript
- `spring` — Retiré du générateur Rails 7+, peut causer des bugs subtils
- `mandrill_mailer` — Mandrill (Mailchimp Transactional) ; vérifier la pérennité du service
- `rspec-rails ~> 3.5` — Très ancien ; rspec-rails 4.x ou 5.x recommandé
- `active_material ~> 1.5` — Thème ActiveAdmin ; vérifier la compatibilité avec ActiveAdmin 3.x si mise à jour

**Risque si non corrigé** :
Gems non maintenues = pas de correctifs. Incompatibilités futures avec Ruby/Rails.

**Recommandation** :
Migrer CoffeeScript vers JavaScript/Typecript (ou supprimer si peu utilisé). Remplacer spring par bootsnap seul. Mettre à jour rspec-rails. Évaluer mandrill_mailer vs Action Mailer + SendGrid/Postmark.

**Bénéfice attendu** :
Stack moderne, moins de dette technique.

---

### 🟠 ARCH-006 — Callbacks : nombre acceptable mais à surveiller

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐

**Localisation** : `app/models/`

**Constat** :
- Order : 2 callbacks (before_validation, before_update)
- Notification : 1 (after_commit send_push_notifications!)
- Invoice : 1 (before_destroy)
- EmailPasswordAuthenticable : 2 (before_validation)
- PushNotification : 1 (after_create_commit schedule)
- Default : 1 (before_validation)

Aucun model n'excède 5 callbacks. Cependant, `Notification#send_push_notifications!` et `PushNotification#schedule` déclenchent des effets de bord importants (envoi de notifications, planification de jobs). Ces callbacks pourraient être explicites dans des services.

**Recommandation** :
Garder les callbacks simples. Pour les effets de bord complexes (notifications), envisager des services appelés explicitement après create/commit, pour plus de visibilité et de testabilité.

**Bénéfice attendu** :
Comportement plus prévisible, tests plus simples.

---

### 🟡 ARCH-007 — API versioning présent (api/v1)

**Sévérité** : Mineur (positif) | **Effort** : — | **Vendabilité** : —

**Localisation** : `config/routes.rb`, `app/controllers/api/v1/`

**Constat** :
L'API REST est versionnée (`api/v1`). Bonne pratique pour l'évolution sans casser les clients existants.

**Recommandation** :
Maintenir le versioning. Documenter la politique de dépréciation si v2 est introduite.

---

### 🟡 ARCH-008 — GraphQL sans versioning explicite

**Sévérité** : Mineur | **Effort** : M (1-3j) | **Vendabilité** : ⭐

**Localisation** : `app/graphql/`

**Constat** :
L'API GraphQL n'a pas de versioning (un seul schéma). Les changements breaking (champs supprimés, types modifiés) impactent tous les clients.

**Recommandation** :
Documenter les changements. Envisager des champs dépréciés avec `deprecation_reason` avant suppression. Pour une évolution majeure, un second schéma (v2) pourrait être introduit.

**Bénéfice attendu** :
Évolution contrôlée de l'API GraphQL.

---

### 🟡 ARCH-009 — Structure Admin (ActiveAdmin) chargée

**Sévérité** : Mineur | **Effort** : — | **Vendabilité** : —

**Localisation** : `app/admin/`

**Constat** :
21 fichiers ActiveAdmin. Personnalisations importantes (mapotempo, recapitulatif, ebp_gestion). La logique métier dans les blocks ActiveAdmin (panel, action_item) peut devenir difficile à maintenir.

**Recommandation** :
Extraire la logique complexe des blocks Admin vers des services ou des presenters. Garder les Admin files légers (déclaration de ressources, configuration).

**Bénéfice attendu** :
Admin plus maintenable.

---

### 🟡 ARCH-010 — Absence de monitoring applicatif

**Sévérité** : Mineur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : Global

**Constat** :
Barnes est présent (métriques Heroku) mais aucun APM (Application Performance Monitoring) type New Relic, Datadog, Scout. Pas de tracing des requêtes lentes ou des erreurs.

**Recommandation** :
Envisager un APM pour la production. Au minimum, des logs structurés (rails_semantic_logger) et des alertes sur les erreurs 5xx.

**Bénéfice attendu** :
Détection proactive des problèmes en production.

---

## Synthèse du domaine

L'architecture présente des forces (API versionnée, services pour certains domaines) mais des faiblesses structurelles : ratio services/models faible, couverture de tests insuffisante, patterns manquants (Form Objects, Policies), Rails EOL, dépendances obsolètes. Les callbacks sont maîtrisés. Le monitoring applicatif est absent.

### Quick wins identifiés dans ce domaine
- ARCH-004 — Planifier migration Rails 6.1+ (M)
- ARCH-005 — Mettre à jour rspec-rails, évaluer coffee-rails (S)
- ARCH-010 — Introduire un APM ou monitoring de base (S)

### Chantiers structurants
- ARCH-001 — Enrichir la couche Service (M)
- ARCH-002 — Augmenter la couverture de tests (L)
- ARCH-003 — Introduire Form Objects, Query Objects, Policies (L)
- ARCH-006 — Réviser les callbacks à effet de bord (S)
