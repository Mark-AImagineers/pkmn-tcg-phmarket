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

---

## 📌 Planned Development Milestones (High-Level, Non-To-Do)

These are all the major building blocks envisioned for the project, based on the full feature map. This list will evolve — some may change, combine, or be postponed — but everything here reflects the real, thoughtful intention behind the product.

---

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
