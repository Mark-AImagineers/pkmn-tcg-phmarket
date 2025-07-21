# 📓 CHANGELOG

This project uses **semantic versioning**:  
`MAJOR.MINOR.PATCH` — where:

- **MAJOR** versions break backward compatibility
- **MINOR** versions add functionality in a backward-compatible manner
- **PATCH** versions are for bug fixes and small tweaks

Each changelog entry is dated and documented clearly for transparency as part of building this project in public.

---

## [0.1.0] – 2025-07-15

### Added
- ✍️ Initial project documentation:
  - `README.md`
  - `CHANGELOG.md`
  - Feature plan, tech stack, contributing guidelines


## [0.1.1] - 2025-07-17

### Added
 - Django project initialized with modular settings
 - Environment loading via `version.json` (`local`, `staging`, `production`)
 - Dockerized dev setup with:
    - Django 5.0.6 + Postgres 15
    - `docker-compose` for local dev
    - `.env` file for secrets and DB config

### Changed
 - Refactored settings into `base.py`, `local.py`, and dynamic `__init__.py`


## [0.1.2] – 2025-07-18

### Added
- Custom user model with email-based login
- Session-based login using Django + HTMX (form, service, view)
- `/api/login/` and `/api/token/refresh/` DRF endpoints using SimpleJWT
- API schema generation with drf-spectacular
- Swagger UI available at `/api/docs/`
- Version dynamically loaded from `version.json` into OpenAPI docs

### Changed
- Split `users/urls.py` (HTMX views) and `users/api_urls.py` (DRF API)

## [0.1.3] - 2025-07-19

### Changed
- Revamped login page styles and background gradients

## [0.1.4] - 2025-07-21

### Removed
- Tailwind CSS and all Node-related files for a leaner Python-only stack

## [0.1.5] - 2025-07-22

### Changed
- Switched styling approach to vanilla CSS
- Updated documentation to reflect simple, clean design for early development

## [0.1.6] - 2025-07-23

### Changed
- Login page now submits credentials to the DRF JWT endpoint via HTMX
- Simplified login HTML and CSS to remove old Tailwind classes

## [0.1.7] - 2025-07-24

### Changed
- Default Postgres host set to `db` for Docker Compose
- Added `.env.example` and Docker setup notes in `README.md`



---
## [0.1.8] - 2025-07-25

### Fixed
- Removed trailing comma in `version.json` which caused startup failure

## [0.1.9] - 2025-07-26

### Added
- Basic user registration with DRF endpoint
- Registration form and page with success/error messages

## [0.1.10] - 2025-07-27

### Added
- `/api/me/` endpoint for retrieving the authenticated user's details

## [0.1.11] - 2025-07-28

### Added
- Basic homepage restricted to logged-in users
- Reusable sidebar component displayed on most pages
- Sidebar displays the authenticated user's email via `/api/me/`

## [0.1.12] - 2025-07-29

### Added
- Header with user icon and greeting
- `/profile/` page for logged-in users

---

## [0.1.13] - 2025-07-30

### Added
- Settings page with admin panel for superusers

---

## [0.1.14] - 2025-07-31

### Fixed
- Session-based login now properly redirects to the homepage

---

## 📌 Planned Development Milestones (High-Level, Non-To-Do)

These are all the major building blocks envisioned for the project, based on the full feature map. This list will evolve — some may change, combine, or be postponed — but everything here reflects the real, thoughtful intention behind the product.

---

### User Management
 - Login, Logout, Registration View
 - Password Reset
 - Profile View
 - User Serializers / Forms
 - Custom User Model
 - Email verification or Social Login Logic

### 🗃 Global Cards Database

- Pull card data from PokéTCG API and keep it in sync
- Manual DB override (Edit/Delete/Seed)
- Visual DB browser in frontend
- Visual set explorer (card gallery like JustInBasil)
- Individual card view with price history
- Tag system (rarity, type, holo, promos, etc.)
- DB backup/export tooling
- Internal admin view for card management
- Quick search and filters by set/type/rarity
- Pagination & lazy loading support

---

### 📁 User Card Collection

- CRUD for personal cards
- Attach custom fields (condition, location, notes)
- Binder-style visual layout
- Portfolio summary dashboard (value, count, stats)
- Import/export via CSV or JSON
- Compare collection vs. full set
- Mark cards as for trade/sale
- Inline card scanner integration (future)
- Private vs. public binders
- Showcase profile view (public collection display)

---

### 🛒 Social Marketplace

- User profiles (nickname, location, binder link)
- Trade Board: list cards for trade
- Sale Board: list cards for sale
- "Looking For" (LF) section
- Post comments, tag others, reply system
- Buyer/seller negotiation DM or comment thread
- Sort/filter: price, location, trade/sale
- Transaction flags (available, pending, done)
- Save favorite sellers/boards

---

### 🔐 Trust & Verification System

- Basic user verification (email, phone, socials)
- User feedback system (star, comment, tag)
- Card verification (photo uploads, serial matching, manual trust)
- Verified seller badge
- Flag/report fraudulent posts
- Escrow/payment trust system (future layer)
- Admin/moderator tools

---

### 🧠 AI Tools & OCR

- Webcam-based card scanner for browser
- Mobile camera scanner integration (later)
- Card edge + text detection with OpenCV
- YOLOv8 object detection for card type
- OCR via Tesseract for name/set recognition
- ML-based card guessing (partial scans, poor lighting)
- Collection value estimation via ML pricing trends

---

### 📊 Analytics & Smart Tools

- Portfolio valuation over time
- Alerts for price drops/rises
- Suggested cards to complete sets
- Trade value matcher (fair trade checks)
- Market sentiment tags (meta, hype, rising)
- Most traded cards / hot cards board

---

### ⚙️ Internal Systems & Dev Infra

- Full test coverage using Pytest
- Dockerized dev environment
- Auto-rebuild + local preview setup
- Admin dashboard for superusers
- Background jobs (for sync, analytics)
- API-first design for mobile/web clients
- HTMX-based interactive frontend
- Modular service-based folder structure
- CI/CD deployment to Heroku

---
