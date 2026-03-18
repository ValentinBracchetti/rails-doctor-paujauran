# Rails Doctor — Profil du Projet

**Date de l'audit** : 18 mars 2025
**Projet** : pjr-rails
**Chemin** : c:\Users\vbrac\Desktop\code\Poujauran\pjr-rails

---

## Identité technique

| Paramètre | Valeur |
|-----------|--------|
| Version de Rails | 6.0.6 |
| Version de Ruby | >= 3.1.2 |
| Base de données | PostgreSQL |
| Serveur web | Puma 5.6 |
| Background jobs | Sidekiq + sidekiq-scheduler |
| Cache store | Dalli (Memcached) — non configuré en production |
| File storage | AWS S3 (Active Storage) |
| Frontend | ActiveAdmin (ERB), API JSON (Jbuilder), GraphQL, CoffeeScript |

---

## Dimensionnement

| Métrique | Nombre |
|----------|--------|
| Models | 31 |
| Controllers | 7 |
| Views | 10 |
| Services | 3 |
| Jobs | 5 |
| Mailers | 2 |
| Tables en base | 29 |
| Routes | ~30 (ActiveAdmin + API + GraphQL) |
| Gems (Gemfile) | ~50 |
| Fichiers de test | 9 |

---

## Gems notables

### Framework & Core
- `rails` (6.0.6) — Framework principal
- `puma` (5.6) — Serveur web
- `pg` (1.5) — Driver PostgreSQL
- `bootsnap` — Optimisation du chargement

### Authentification & Autorisation
- `devise` — Admin users
- `devise-i18n` — Traductions Devise
- `activeadmin` — Interface d'administration

### API & Serialization
- `graphql` — API GraphQL
- `graphiql-rails` — Interface GraphiQL
- `jbuilder` — Serialisation JSON
- `rack-cors` — CORS pour API

### Background Processing
- `sidekiq` — Jobs asynchrones
- `sidekiq-scheduler` — Jobs planifiés

### Monitoring & Logging
- `rails_semantic_logger` — Logging structuré
- `audited` — Audit trail
- `barnes` — Métriques Heroku

### Testing
- `rspec` / `rspec-rails` (3.5)
- `factory_bot_rails`
- `capybara`
- `brakeman` / `bundle-audit` — Audit sécurité

---

## Patterns architecturaux détectés

- [x] Service Objects (`app/services/`) — 3 services (Crypto, Expo Push, Twilio)
- [ ] Query Objects (`app/queries/`)
- [ ] Form Objects (`app/forms/`)
- [ ] Presenters / Decorators (`app/presenters/` ou `app/decorators/`)
- [ ] Policy Objects (`app/policies/`)
- [ ] Value Objects (`app/values/`)
- [ ] Rails Engines (`engines/`)
- [x] API mode — `config.api_only = true` (avec ActiveAdmin en overlay)
- [ ] Hotwire / Turbo / Stimulus
- [x] Namespacing par domaine métier — `api/v1`, `admin`

---

## Observations préliminaires

- **Architecture hybride** : Application configurée en `api_only` mais inclut ActiveAdmin (views ERB, assets CoffeeScript/SCSS). Sprockets non chargé explicitement dans application.rb (commenté).
- **Authentification double** : Devise pour les admin_users, authentification par token custom (AccessToken) pour l'API mobile.
- **GraphQL** : Endpoint `/graphql` exposé, GraphiQL activable via `ENABLE_GRAPHIQL`.
- **Sidekiq Web** : Monté conditionnellement via `ENV['SIDEKIQ_WEB_PATH']` — à vérifier l'authentification.
- **Dépendances** : Rails 6.0 en EOL (juin 2023), coffee-rails obsolète, mandrill_mailer, spring.
- **Cache** : Dalli présent mais `config.cache_store` commenté en production.

---

*Ce profil sert de base pour les phases d'analyse détaillée qui suivent.*
