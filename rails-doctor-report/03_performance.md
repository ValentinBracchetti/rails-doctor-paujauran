# ⚡ Performance

**Score du domaine** : 10 / 20

---

## Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | 1 |
| 🟠 Majeur | 4 |
| 🟡 Mineur | 3 |
| 🔵 Cosmétique | 0 |

**Outils utilisés** : Analyse manuelle (grep, lecture schema, types GraphQL)

---

## Findings

### 🔴 PERF-001 — Absence de la gem Bullet pour détecter les N+1

**Sévérité** : Critique | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `Gemfile` — Bullet absente

**Constat** :
Aucun outil n'est en place pour détecter les requêtes N+1 en développement. Les développeurs ne sont pas alertés lors de l'introduction de N+1.

**Risque si non corrigé** :
Les N+1 passent en production inaperçus. Sous charge, chaque N+1 multiplie le temps de réponse par le nombre d'enregistrements. Une liste de 50 commandes avec N+1 sur product_items peut générer des centaines de requêtes.

**Recommandation** :
Ajouter `gem 'bullet', group: :development` et configurer dans `config/environments/development.rb` :
```ruby
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.bullet_logger = true
  Bullet.console = true
end
```

**Bénéfice attendu** :
Détection proactive des N+1 avant mise en production. Réduction des incidents de performance.

---

### 🟠 PERF-002 — N+1 potentiels dans les types GraphQL (Order, Client)

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `app/graphql/types/order_type.rb`, `app/graphql/types/client_type.rb`, `app/graphql/types/query_type.rb`

**Constat** :
- **OrderType** expose `client`, `products` (via product_items), `subscription`. Lors d'une requête `orders(client_id: X)`, chaque order charge séparément son client, ses product_items/products, sa daily_subscription.
- **ClientType** expose `comments`, `invoices`, `current_catalog_products`. Une liste de clients déclenche une requête par client pour chaque association.
- **QueryType#orders** retourne `client.orders` sans `includes`. Les résolveurs GraphQL chargent les associations à la demande (lazy) — chaque field peut déclencher une requête.

**Risque si non corrigé** :
Requêtes GraphQL lentes sur les listes. Ex. `orders { id client { name } products { name } }` sur 20 commandes = 1 + 20 + 20 + 20 = 61+ requêtes au lieu de 4 avec des includes appropriés.

**Recommandation** :
Utiliser `GraphQL::Batch` ou `graphql-batch` pour le batching des requêtes. Ou précharger dans les résolveurs : `Order.includes(:client, product_items: :product, daily_subscription: :subscription).where(...)`. Pour ClientType, utiliser un DataLoader ou inclure les associations dans la requête parente.

**Bénéfice attendu** :
Réduction drastique du nombre de requêtes sur les requêtes GraphQL listant des orders ou clients.

---

### 🟠 PERF-003 — Cache store non configuré en production

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `config/environments/production.rb` (ligne 54)

**Constat** :
`config.cache_store = :mem_cache_store` est commenté. Dalli (Memcached) est dans le Gemfile mais non configuré. Rails utilise donc le `:memory_store` par défaut — non partagé entre processus, perdu au redémarrage.

**Risque si non corrigé** :
Aucun cache applicatif efficace. Les fragment caches et `Rails.cache` ne persistent pas. Chaque requête recalcule tout. Sous charge, la base de données et l'application sont sollicitées inutilement.

**Recommandation** :
Décommenter et configurer :
```ruby
config.cache_store = :mem_cache_store, ENV.fetch("MEMCACHE_SERVERS", "localhost:11211").split(",")
```
Ou utiliser Redis si déjà en place pour Sidekiq : `config.cache_store = :redis_cache_store, { url: ENV["REDIS_URL"] }`

**Bénéfice attendu** :
Cache partagé et persistant. Possibilité d'utiliser le fragment caching et `Rails.cache` pour les données fréquemment lues.

---

### 🟠 PERF-004 — Pas de fragment caching dans les vues

**Sévérité** : Majeur | **Effort** : M (1-3j) | **Vendabilité** : ⭐⭐

**Localisation** : `app/views/`, `app/admin/`

**Constat** :
Aucun `cache do ... end` ou `cache @model` trouvé dans les vues. Les vues Admin (ActiveAdmin) et API (Jbuilder) sont régénérées à chaque requête.

**Risque si non corrigé** :
Pages admin lourdes (listes de commandes, clients, factures) recalculent tout à chaque visite. Pas de Russian doll caching pour les listes.

**Recommandation** :
Identifier les vues les plus coûteuses (ex. dashboard, listes). Ajouter `cache [model, model.updated_at]` pour les fragments stables. Activer le cache store (PERF-003) avant.

**Bénéfice attendu** :
Réduction de la charge serveur sur les pages admin consultées fréquemment.

---

### 🟠 PERF-005 — QueryType#all_clients et #client : Client.all sans optimisation

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐

**Localisation** : `app/graphql/types/query_type.rb` (lignes 51-63)

**Constat** :
`Client.ordered` et `Client.all` sont retournés sans `includes`. Lorsque ClientType résout `comments`, `invoices`, `current_catalog_products`, chaque client déclenche des requêtes supplémentaires.

**Risque si non corrigé** :
Une requête `all_clients { id name comments { body } }` sur 100 clients = 1 + 100 requêtes pour les comments (au minimum).

**Recommandation** :
Précharger les associations selon les champs demandés (GraphQL permet de connaître les champs sélectionnés). Ou utiliser un DataLoader. Pour une première approche : `Client.ordered.includes(:active_admin_comments)` si comments est souvent demandé.

**Bénéfice attendu** :
Moins de requêtes sur les listes de clients.

---

### 🟡 PERF-006 — Index potentiellement manquants

**Sévérité** : Mineur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : `db/schema.rb`

**Constat** :
La plupart des foreign keys ont des index. Vérifications :
- `invoices` : pas de colonne `client_id` directe ; `status` (enum) utilisé dans les scopes — index présent sur `invoice_num`, `invoice_ref`
- `notifications` : `target_type`, `target_id` indexés ; `happened_at` utilisé pour order — pas d'index dédié
- `audits` : `user_id`, `user_type` dans user_index ; `auditable_id` dans auditable_index
- `group_memberships` : index sur member_type/member_id, group_type/group_id, group_name

Les index semblent corrects. Un index composite sur `notifications (target_type, target_id, happened_at)` pourrait aider `Notification.for_user(...).order(happened_at: :desc)`.

**Recommandation** :
Analyser les requêtes lentes en production (logs, APM). Ajouter des index ciblés si des full table scans sont identifiés.

**Bénéfice attendu** :
Optimisation des requêtes les plus fréquentes.

---

### 🟡 PERF-007 — Emails : deliver_later utilisé (positif)

**Sévérité** : Mineur (positif) | **Effort** : — | **Vendabilité** : —

**Localisation** : `app/controllers/api/v1/users_controller.rb`

**Constat** :
`UserMailer.welcome_new_user(@user).deliver_later` et `reset_password_email(...).deliver_later` — les emails sont envoyés en asynchrone via Sidekiq. Bonne pratique.

**Recommandation** :
Maintenir cette approche pour tous les envois d'emails.

---

### 🟡 PERF-008 — Jobs planifiés : exécution synchrone possible

**Sévérité** : Mineur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐

**Localisation** : `app/jobs/`

**Constat** :
Les jobs (DailyCreateOrdersJob, DailyValidateOrdersJob, etc.) sont conçus pour Sidekiq. Vérifier que `perform_later` est bien utilisé partout et qu'aucun `perform_now` n'est appelé en production pour ces jobs lourds.

**Recommandation** :
Audit des appels aux jobs. S'assurer que les jobs planifiés (sidekiq-scheduler) et manuels utilisent `perform_later`.

---

## Synthèse du domaine

Les principaux points de performance sont : l'absence de Bullet (détection N+1), les N+1 probables dans GraphQL (OrderType, ClientType), le cache non configuré en production, et l'absence de fragment caching. Les emails sont correctement envoyés en asynchrone. Les index de base semblent corrects ; une analyse en production affinera les besoins.

### Quick wins identifiés dans ce domaine
- PERF-001 — Ajouter Bullet (XS)
- PERF-003 — Configurer cache_store en production (S)
- PERF-005 — Précharger associations dans QueryType clients (XS)

### Chantiers structurants
- PERF-002 — Résoudre les N+1 GraphQL (OrderType, ClientType) avec Batch/DataLoader (S)
- PERF-004 — Introduire le fragment caching (M)
- PERF-006 — Analyser et ajouter index si nécessaire (S)
