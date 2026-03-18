# 🧹 Qualité de code

**Score du domaine** : 12 / 20

---

## Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | 2 |
| 🟠 Majeur | 5 |
| 🟡 Mineur | 8 |
| 🔵 Cosmétique | 3 |

**Outils utilisés** : RuboCop, Reek, Flog, rails_best_practices

---

## Findings

### 🔴 CQ-001 — Mutation UpdateClient : méthode monolithique (52 paramètres, 57 statements)

**Sévérité** : Critique | **Effort** : M (1-3j) | **Vendabilité** : ⭐⭐

**Localisation** : `app/graphql/mutations/update_client.rb` (lignes 61-174)

**Constat** :
La mutation `UpdateClient#resolve` accepte 52 arguments et contient ~57 statements. Score Flog 100.3 (seuil critique > 60). FeatureEnvy massif sur l'objet `client`. DuplicateMethodCall sur `client_code.nil?`, `director.nil?`, etc.

**Risque si non corrigé** :
Maintenance extrêmement difficile. Chaque ajout de champ Client nécessite de modifier la mutation. Risque de régressions élevé. Tests complexes à écrire.

**Recommandation** :
Introduire un Form Object ou Input Object GraphQL structuré (ex. `ClientAttributesInput`). Grouper les attributs par domaine (adresse, horaires, contacts). Utiliser `client.assign_attributes(params)` avec un hash filtré.

**Bénéfice attendu** :
Réduction de la complexité cyclomatique. Évolution du modèle Client sans toucher à la signature de la mutation.

---

### 🔴 CQ-002 — Law of Demeter violée massivement (mapotempo.rb)

**Sévérité** : Critique | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `app/admin/mapotempo.rb` (lignes 23-74)

**Constat** :
rails_best_practices signale 18 violations de la loi de Déméter. Chaînes d'appels du type `object.a.b.c` ou `object.x.y.z` sur plusieurs lignes. Méthode `csv#humanize_name` avec complexité Flog 41.6.

**Risque si non corrigé** :
Couplage fort aux structures internes. Toute modification des modèles associés casse ce code. Difficile à tester en isolation.

**Recommandation** :
Introduire des méthodes déléguées sur les modèles (ex. `order.client_delivery_address`) ou un Presenter/Decorator pour la vue Mapotempo. Encapsuler les chaînes d'appels dans des méthodes nommées.

**Bénéfice attendu** :
Découplage, testabilité, évolution des modèles sans impact sur l'admin.

---

### 🟠 CQ-003 — Méthodes inutilisées (dead code)

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐

**Localisation** : Multiple (Client, Invoice, Order, Notification, etc.)

**Constat** :
rails_best_practices identifie 20+ méthodes "unused" : `Client#image_url`, `Client#available_products`, `Client#current_catalog_products`, `Invoice#unknown`, `Invoice#edited`, `Order#ordered_by_client`, `Order#too_late_to_change?`, `User#default_client`, etc. Certaines peuvent être des helpers pour vues ou des méthodes appelées dynamiquement — à vérifier.

**Risque si non corrigé** :
Code mort augmente la dette cognitive. Confusion pour les développeurs. Possible utilisation future non documentée.

**Recommandation** :
Audit manuel avec `grep` pour confirmer l'absence d'appel. Supprimer ou marquer `# TODO: used by X` si usage indirect. Envisager des scopes nommés pour remplacer certaines méthodes.

**Bénéfice attendu** :
Codebase plus claire, moins de bruit.

---

### 🟠 CQ-004 — Mutations Order et autres : TooManyStatements, DuplicateMethodCall

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `app/graphql/mutations/order.rb`, `app/graphql/mutations/phone_number_verification.rb`, `app/graphql/types/query_type.rb`

**Constat** :
- `Mutations::Order#resolve` : 16 statements, Flog 48.8, `order.product_items` appelé 3 fois, `pk.quantity` 2 fois
- `Mutations::PhoneNumberVerification#resolve` : `Rails.logger` appelé 2 fois
- `Types::QueryType#basket` : 7 statements, FeatureEnvy sur `client`

**Risque si non corrigé** :
Duplication et complexité inutiles. Mémoïsation manquante pour les appels répétés.

**Recommandation** :
Extraire des méthodes privées. Mémoïser `order.product_items` dans une variable locale. Utiliser `logger ||= Rails.logger` si besoin.

**Bénéfice attendu** :
Code plus lisible, moins de requêtes redondantes.

---

### 🟠 CQ-005 — Jobs : DuplicateMethodCall (Rails.logger, Time.zone.today)

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐

**Localisation** : `app/jobs/daily_create_orders_job.rb`, `daily_needs_validation_notification_job.rb`, `daily_validate_orders_job.rb`

**Constat** :
`Rails.logger` appelé 3-4 fois par job, `Time.zone.today` 2 fois. Reek signale DuplicateMethodCall.

**Risque si non corrigé** :
Overhead mineur. Incohérence de style.

**Recommandation** :
`today = Time.zone.today` en début de méthode. `logger = Rails.logger` si plusieurs appels.

**Bénéfice attendu** :
Code plus propre, légère optimisation.

---

### 🟠 CQ-006 — Models : FeatureEnvy, TooManyStatements (Import, Invoice, InvoiceGroup)

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `app/models/import.rb`, `app/models/invoice.rb`, `app/models/invoice_group.rb`

**Constat** :
- `Import#execute_now` : 12 statements, Flog 28.4
- `Import#attribute_for_line` : 7 statements, FeatureEnvy sur `line`
- `Invoice#populate_items` : NestedIterators, 7 statements
- `InvoiceGroup#submit!` : 23.1 Flog, FeatureEnvy sur `p`

**Risque si non corrigé** :
Logique métier difficile à isoler et tester. Méthodes trop longues.

**Recommandation** :
Extraire des services ou des méthodes privées. `Import` pourrait déléguer à des classes `ImportLineParser`, `ImportExecutor`.

**Bénéfice attendu** :
Séparation des responsabilités, testabilité.

---

### 🟠 CQ-007 — Use scope access (UsersController)

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐

**Localisation** : `app/controllers/api/v1/users_controller.rb` (ligne 52)

**Constat** :
rails_best_practices signale "use scope access" — probablement un `User.find` ou `User.where` qui pourrait utiliser un scope nommé.

**Risque si non corrigé** :
Logique de requête dupliquée dans le controller. Moins de réutilisabilité.

**Recommandation** :
Créer un scope sur le modèle User et l'utiliser dans le controller.

**Bénéfice attendu** :
Cohérence, réutilisation.

---

### 🟡 CQ-008 — RuboCop : 0 offenses

**Sévérité** : Mineur (positif) | **Effort** : — | **Vendabilité** : —

**Constat** :
RuboCop ne signale aucune offense sur app/ et lib/. Le projet respecte les conventions configurées.

**Recommandation** :
Maintenir cette configuration. Ajouter rubocop-performance si pertinent.

---

### 🟡 CQ-009 — Noms de variables non communicatifs (e, v, p, t, a, i, c)

**Sévérité** : Mineur | **Effort** : M (1-3j) | **Vendabilité** : ⭐

**Localisation** : Multiple (GraphQL mutations, models, services)

**Constat** :
Reek signale `UncommunicativeVariableName` : `e` (exception), `v` (variable), `p` (paramètre), `t` (token), `a` (array), `i` (index), `c` (client), etc. Une trentaine d'occurrences.

**Risque si non corrigé** :
Lisibilité réduite. `e` pour exception est acceptable, mais `p`, `a`, `i` dans des contextes complexes sont ambigus.

**Recommandation** :
Renommer progressivement : `e` → `error`, `p` → `params` ou `product`, `a` → `attributes`, etc.

**Bénéfice attendu** :
Meilleure lisibilité.

---

### 🔵 CQ-010 — IrresponsibleModule (absence de documentation)

**Sévérité** : Cosmétique | **Effort** : L (3-10j) | **Vendabilité** : ⭐

**Constat** :
Reek signale ~80 occurrences de `IrresponsibleModule` — classes/modules sans commentaire descriptif.

**Recommandation** :
Ajouter des commentaires YARD ou des docstrings au fil des modifications. Prioriser les modules publics (API, GraphQL).

---

### 🔵 CQ-011 — Trailing whitespace (migrations, vues)

**Sévérité** : Cosmétique | **Effort** : XS (< 2h) | **Vendabilité** : ⭐

**Localisation** : `app/views/admin/orders/new_invoices.html.erb`, migrations (6 fichiers)

**Recommandation** :
`bundle exec rubocop -a` ou suppression manuelle.

---

### 🔵 CQ-012 — DataClump (ProductionOrder)

**Sévérité** : Cosmétique | **Effort** : S (2-8h) | **Vendabilité** : ⭐

**Localisation** : `app/models/production_order.rb`

**Constat** :
Les paramètres `baking` et `delivery_round` sont passés ensemble à 4 méthodes. Reek signale DataClump.

**Recommandation** :
Introduire un Value Object ou un struct `ProductionContext(baking:, delivery_round:)`.

---

## Synthèse du domaine

La qualité de code est globalement correcte (RuboCop propre) mais des points critiques existent : la mutation `UpdateClient` est monolithique, et la loi de Déméter est violée dans `mapotempo.rb`. Les méthodes inutilisées et les DuplicateMethodCall sont des quick wins. Le reste (documentation, noms de variables) est cosmétique.

### Quick wins identifiés dans ce domaine
- CQ-005 — Mémoïser Rails.logger et Time.zone dans les jobs (XS)
- CQ-007 — Use scope access dans UsersController (XS)
- CQ-011 — Supprimer trailing whitespace (XS)

### Chantiers structurants
- CQ-001 — Refactorer UpdateClient en Form Object (M)
- CQ-002 — Corriger Law of Demeter dans mapotempo (S)
- CQ-003 — Supprimer les méthodes inutilisées (S)
- CQ-004 — Refactorer mutations Order et QueryType (S)
- CQ-006 — Extraire logique Import/Invoice (S)
