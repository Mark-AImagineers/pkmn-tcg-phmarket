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

---

## [0.1.4] - 2025-07-21

### Removed
- Tailwind CSS and all Node-related files for a leaner Python-only stack

### Changed
- Switched styling approach to vanilla CSS
- Updated documentation to reflect simple, clean design for early development
- Login page now submits credentials to the DRF JWT endpoint via HTMX
- Simplified login HTML and CSS to remove old Tailwind classes
- Default Postgres host set to `db` for Docker Compose
- Added `.env.example` and Docker setup notes in `README.md`

### Fixed
- Removed trailing comma in `version.json` which caused startup failure

### Added
- Basic user registration with DRF endpoint
- Registration form and page with success/error messages
- `/api/me/` endpoint for retrieving the authenticated user's details
- Basic homepage restricted to logged-in users
- Reusable sidebar component displayed on most pages
- Sidebar displays the authenticated user's email via `/api/me/`

---

## [0.2.10] - 2025-07-22

### Added
- Header with user icon and greeting
- `/profile/` page for logged-in users
- Settings page with admin panel for superusers
- Logout button on the homepage to clear tokens and redirect to login
- Admin panel button to send a test email using environment settings
- Password reset API and pages
- Password reset now notifies when the email doesn't exist and links to registration
- Skeleton cards app with admin view for managing global cards
- Card models for sets, cards, attacks, weaknesses, and pricing
- Serializers for all card models
- Sync endpoint to update cards from PokéTCG
- Button on manage cards page to trigger sync

### Fixed
- Session-based login now properly redirects to the homepage
- Password reset link parsing on confirmation page
- Optional show password toggles on login, registration, and reset pages
- Release dates from PokéTCG API now handle `YYYY/MM/DD` format correctly

### Changed
- Removed all session-based authentication logic
- HTMX now sends JWT tokens with every request and `/api/me/` drives UI state
- Login endpoint now sets the refresh token in a secure HTTP-only cookie
- `/api/token/refresh/` reads the cookie and returns a new access token
- Updated documentation to describe the improved token flow
- Registration and password reset confirmation pages now redirect to the login page upon success

---

## [0.2.14] - 2025-07-24

### Fixed
- 404 error on sync - fixed with longer timer and retry logic

### Changed
- Redid the PokeTCG logic, split into discovery and sync logics
- CardRef model created to sync card ids first (discovery)
- Sync logic now runs through DB check before calling API endpoint

## [0.2.17] - 2025-07-25

### Added
- Admin page now provides buttons to:
  - discover card IDs from PokéTCG
  - sync all missing cards
  - sync a limited number of cards
- Reusable `base.html` layout with header and sidebar includes
- `/static/css/base.css` with clean layout structure (sidebar, header, content)
- `/static/js/auth.js` for shared auth greeting + HTMX token injection
- `/static/js/logout.js` for consistent logout logic
- Home page now uses the new layout and includes logout functionality
- Unified base layout with full-width topbar and fixed sidebar using Flexbox
- `core/_header.html` partial to display user email, name, and avatar in the header
- `static/css/base.css` updated with clear layout zones (header, sidebar, main)
- `auth.css` created to style all auth-related pages (glassmorphic dark theme)
- Shared token logic centralized in `auth.js` for greeting + protection

### Changed
- New API endpoints for the updated card discovery and sync logic
- Sidebar and header extracted into partials: `_sidebar.html` and `_header.html`
- Settings updated to include global `templates/` folder in `TEMPLATES['DIRS']`
- `base.html` now wraps content in `.main-layout` with `header + sidebar + main`
- Header restyled with:
  - `#d9d9d9` background
  - Small email text, bold welcome text
  - Avatar with white circular border
- Sidebar layered above topbar via `z-index`
- Redirect logic added to `/api/me/` fetch to handle expired JWTs and fallback to login
- `home.html` now uses new layout and logout flow
- `login.html`, `register.html`, and `password_reset_confirm.html` now use shared `auth.css` and clean markup

### Fixed
- Template load error caused by `{% load static %}` above `{% extends %}` in `home.html`
- Timeout behavior when token fetch fails — now auto-redirects to `/login/`

### Note
- This marks the start of the new front-end foundation for all MVP features
- Pages are now modular, readable, and style-consistent.
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

## [0.2.18] - 2025-07-25

### Fixed
- Login page now handles cookie-based refresh token correctly

## [0.2.19] - 2025-07-25

### Fixed
- Sidebar and header now stay fixed while the main content scrolls

