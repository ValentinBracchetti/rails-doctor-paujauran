# 🔒 Sécurité

**Score du domaine** : 8 / 30

---

## Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | 4 |
| 🟠 Majeur | 12 |
| 🟡 Mineur | 8 |
| 🔵 Cosmétique | 0 |

**Outils utilisés** : bundler-audit, vérifications manuelles (Brakeman non exécutable sur Windows — Process.fork non supporté)

---

## Findings

### 🔴 SEC-001 — CVE GraphQL : exécution de code à distance

**Sévérité** : Critique | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `graphql` gem (2.0.14)

**Constat** :
CVE-2025-27407 (GHSA-q92j-grw3-h492) — Critical. La gem graphql permet l'exécution de code à distance lors du chargement d'un schéma GraphQL malveillant.

**Risque si non corrigé** :
Un attaquant peut exécuter du code arbitraire sur le serveur en soumettant une requête GraphQL crafted. Compromission totale de l'application et des données.

**Recommandation** :
Mettre à jour graphql vers `>= 2.0.32` : `bundle update graphql`

**Bénéfice attendu** :
Élimination d'une vulnérabilité critique permettant la prise de contrôle du serveur.

---

### 🔴 SEC-002 — SSL désactivé en production

**Sévérité** : Critique | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `config/environments/production.rb` (ligne 40)

**Constat** :
`config.force_ssl = true` est commenté. Les requêtes HTTP ne sont pas redirigées vers HTTPS. Les cookies et tokens peuvent transiter en clair.

**Risque si non corrigé** :
Interception des sessions, tokens d'authentification et données sensibles (man-in-the-middle). Non-conformité RGPD pour les données personnelles.

**Recommandation** :
Décommenter la ligne : `config.force_ssl = true`

**Bénéfice attendu** :
Chiffrement de toutes les communications. Conformité aux bonnes pratiques de sécurité.

---

### 🔴 SEC-003 — CVE ActiveAdmin : XSS stocké et injection CSV

**Sévérité** : Critique | **Effort** : M (1-3j) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `activeadmin` gem (2.12.0)

**Constat** :
- CVE-2024-37031 : XSS stocké dans les légendes de formulaires dynamiques (High)
- CVE-2023-51763 : Injection CSV (High)

**Risque si non corrigé** :
Usurpation de session admin, vol de credentials, exécution de scripts malveillants. Export CSV manipulable pour injection de formules Excel.

**Recommandation** :
Mettre à jour ActiveAdmin vers `>= 3.2.2` ou `>= 4.0.0.beta7`. Attention aux breaking changes (API v4).

**Bénéfice attendu** :
Interface d'administration sécurisée contre XSS et injection CSV.

---

### 🔴 SEC-004 — CVE ActiveRecord : injection SQL

**Sévérité** : Critique | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `activerecord` (6.0.6)

**Constat** :
CVE-2023-22794 (GHSA-hq7p-j377-6v63) — High. Vulnérabilité d'injection SQL via les commentaires ActiveRecord.

**Risque si non corrigé** :
Extraction, modification ou suppression de données. Bypass des contrôles d'accès. Sanctions RGPD.

**Recommandation** :
Mettre à jour Rails vers `>= 6.1.7.1` (ou 7.x). Planifier une migration Rails 6.0 → 6.1.

**Bénéfice attendu** :
Élimination d'une faille SQL critique dans le cœur de l'ORM.

---

### 🟠 SEC-005 — Log level debug en production

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐⭐

**Localisation** : `config/environments/production.rb` (ligne 44)

**Constat** :
`config.log_level = :debug` expose des informations détaillées (stack traces, requêtes SQL, variables) dans les logs.

**Risque si non corrigé** :
Fuites d'informations sensibles (mots de passe, tokens, structure interne). Surface d'attaque accrue si les logs sont accessibles.

**Recommandation** :
Utiliser `config.log_level = :info` ou `:warn`. S'appuyer sur `ENV["LOG_LEVEL"]` pour le debug ponctuel.

**Bénéfice attendu** :
Réduction de la surface d'information exposée en production.

---

### 🟠 SEC-006 — CORS mal configuré

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐

**Localisation** : `config/initializers/cors.rb` (ligne 10)

**Constat** :
`origins 'example.com'` — valeur placeholder. L'API ne sera pas accessible depuis le frontend réel, ou nécessite une modification manuelle risquée.

**Risque si non corrigé** :
Si modifié en `'*'` par erreur : toute origine peut appeler l'API (CORS bypass). Si laissé en `example.com` : l'API mobile/web ne fonctionne pas correctement.

**Recommandation** :
Configurer les origines réelles via ENV : `origins ENV.fetch('CORS_ORIGINS', '').split(',')` ou liste explicite des domaines autorisés.

**Bénéfice attendu** :
CORS correctement restreint aux domaines légitimes.

---

### 🟠 SEC-007 — Absence de Content Security Policy

**Sévérité** : Majeur | **Effort** : S (2-8h) | **Vendabilité** : ⭐⭐

**Localisation** : Pas de `config/initializers/content_security_policy.rb`

**Constat** :
Aucune Content Security Policy configurée. Les headers CSP ne sont pas envoyés.

**Risque si non corrigé** :
Mitigation réduite contre XSS. Scripts inline et chargements non contrôlés.

**Recommandation** :
Créer l'initializer CSP avec `rails g content_security_policy` ou configuration manuelle des directives.

**Bénéfice attendu** :
Couche de défense supplémentaire contre les attaques XSS.

---

### 🟠 SEC-008 — Secrets development/test en clair dans secrets.yml

**Sévérité** : Majeur | **Effort** : XS (< 2h) | **Vendabilité** : ⭐⭐

**Localisation** : `config/secrets.yml` (lignes 21-24)

**Constat** :
`secret_key_base` pour development et test sont en clair dans le fichier. Si le repo est partagé ou fuit, ces clés sont exposées.

**Risque si non corrigé** :
Fabrication de cookies/sessions valides pour l'environnement de test. Risque si le repo est public ou compromis.

**Recommandation** :
Utiliser `ENV["SECRET_KEY_BASE"]` pour tous les environnements, ou `credentials` pour development/test.

**Bénéfice attendu** :
Aucun secret en clair dans le dépôt.

---

### 🟠 SEC-009 à SEC-020 — Autres CVEs (Rails, Puma, Loofah, etc.)

**Sévérité** : Majeur / Mineur | **Effort** : M-L (mise à jour Rails/gems) | **Vendabilité** : ⭐⭐⭐

**Constat** :
bundle-audit a identifié 40+ vulnérabilités supplémentaires, notamment :
- actionview (XSS contenteditable), actionpack (ReDoS, XSS redirect_to), activestorage (fuite session), activesupport (ReDoS, XSS, file disclosure)
- puma (HTTP smuggling), loofah, rails-html-sanitizer (XSS, ReDoS), rexml (DoS, ReDoS)
- dalli (code injection), devise (race condition), aws-sdk-s3 (key commitment), sidekiq (DoS), globalid (ReDoS), fugit, faraday, thor, net-imap, audited

**Risque si non corrigé** :
Surface d'attaque étendue. Les CVEs publiques sont les premières testées par les attaquants.

**Recommandation** :
Planifier une mise à jour majeure : Rails 6.0 → 6.1 ou 7.x, puis mise à jour des gems dépendantes. Traiter en priorité : graphql, activeadmin, activerecord, puma, loofah, rails-html-sanitizer.

**Bénéfice attendu** :
Réduction drastique des vulnérabilités connues.

---

## Synthèse du domaine

L'application présente des risques de sécurité significatifs : une CVE critique (GraphQL RCE), SSL désactivé, log level trop verbeux, CORS placeholder, absence de CSP, et 40+ CVEs dans les dépendances. La correction des points SEC-001 à SEC-008 (quick wins) est prioritaire. La mise à jour de Rails et des gems (SEC-009+) constitue un chantier structurant.

### Quick wins identifiés dans ce domaine
- SEC-002 — Activer force_ssl (XS)
- SEC-005 — Réduire log_level en production (XS)
- SEC-006 — Configurer CORS correctement (XS)
- SEC-008 — Externaliser les secrets development/test (XS)
- SEC-001 — Mise à jour graphql (S)

### Chantiers structurants
- SEC-003 — Mise à jour ActiveAdmin (M)
- SEC-004 — Migration Rails 6.0 → 6.1+ (S-M)
- SEC-007 — Mise en place CSP (S)
- SEC-009+ — Mise à jour globale des dépendances (L)
