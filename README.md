# Pokémon TCG Market PH

**Catalogue, Trade, and Sell Pokémon cards with fellow Pinoys — fast, easy, and built with trust in mind.**
> Built in public. Made by a Filipino collector, for Filipino collectors.

## 📖 Intro & Vision

**Pokémon TCG Market PH** is an open-source platform for Filipino collectors, players, and sellers to easily catalogue, trade, and sell their Pokémon cards.

This started as a personal project — I wanted a tool where I could scan my physical cards, track my collection, and eventually trade or sell them (securely) with others in the PH community. What started as a simple idea, I'd like to grow it into a full ecosystem: from webcam-based cataloguing, to a trusted marketplace, to future price tracking and collection value monitoring.

The goal is to make card collecting in the Philippines:
- 🧠 Smarter (with data and automation)
- 🔄 Easier (with tools to manage and trade)
- 🤝 Safer (with trust features for local deals)

I'm building this **in public** — with real commits, real transparency, and a strong desire to turn this into something useful for the community. Right now, it’s free and a work-in-progress. Eventually, this could evolve into a paid tool for power users, but the core mission stays the same: **empower the local Pokémon TCG scene**.

## 🧩 Core Features Concept (Updated as of 15.07.2025)

### Global Cards DB 
    - Pull list and update DB from PokeTCG API (https://docs.pokemontcg.io)
    - Edit / Delete Record Manually
    - Backup DB Records
    - Seed DB Record
    - Review DB in UI Frontend
    - Explore Cards from the Set (Visual Set List - Like JustInBasil)
    - Individual Cards Price Tracker

### User Cards DB
    - Create/Read/Update/Delete Cards Manually
    - Import/Export CSV, JSON
    - Cards Portfolio Binder View (Showcase Cards)
    - Cards Portfolio Dashboard (Price Trackers)
    - Individual Cards Price Tracker

### Social Media Market Place
    - User Profile
    - For Sale Board
    - For Trade Board
    - Message Board (LF, QnA, News, Announcements)

### Trust System
    - User Verification
    - Card Authentication

## Future Features to Implement
- Scan Cards using Mobile Phone
- Scan Cards using Webcam (WebApp)
- Deck Builder
- Chatbot LLM
- AI prediction models - applied on analytics

## 🏗️ Development Phases

I'm building this project layer by layer — not feature-hopping, just stacking foundations properly so it actually works. This section shows how it's planned and what’s coming next.

💡 Got ideas or feedback?
This project is being built in public — if you have suggestions, feature ideas, or just want to jam, feel free to open an issue or reach out. Contributions, comments, and crazy ideas are all welcome!
---

## 📓 **Changelog**

Want to see how the project is progressing day by day?
Check out the full build log in [`CHANGELOG.md`](./CHANGELOG.md) — I’m documenting every key commit, update, and decision there as part of building in public.

## 🧰 Tech Stack

This is the current and planned stack powering the project: (May still change in the future)

| Layer         | Tech                                  | Notes                                                                         |
|---------------|---------------------------------------|-------------------------------------------------------------------------------|
| Front End     | Django Templates + HTMX + Vanilla CSS | Simple styles now, server-rendered UI with optional interactivity |
| API Layer     | Django REST Framework (DRF)           | Fuels API endpoints for HTMX calls, frontend features, and future FE clients  |
| Back End      | Django (Python)                       | Core logic, routing, ORM, forms, and service layer logic                      |
| Database      | PostgreSQL                            | Production-grade RDBMS with local/dev SQLite fallback if needed               |
| Auth          | JWT (DRF SimpleJWT)                   | Tokens stored client-side and sent with every HTMX request                     |
| Testing       | Pytest + pytest-django                | Simple, scalable testing framework for Django apps                            |
| Dev Tools     | Docker + VSCode Dev Containers        | Containerized dev environment with editor-level integration                   |
| Deployment    | Heroku                                | Easy fullstack hosting with CI/CD support                                     |
| AI / OCR      | OpenCV + YOLOv8 + Tesseract OCR       | Card scanning, object detection, and text recognition (future feature)        |
| ML / Analytics| PyTorch + scikit-learn + Keras        | For future data analysis, collection valuation, and smart suggestions         |
### Styling Approach
Currently the project uses simple vanilla CSS for styling. Keeping things minimal helps us focus on functionality first. Front-end design and UI/UX improvements are welcome in future phases.
## 🧑‍💻 **About the Build**

This project is maintained by a solo dev (ME) — primarily a Python backend developer, but capable of shipping fullstack. Most of the early focus will be on building solid backend systems and OCR tools before polishing the frontend. (OR whatever feels right at the moment😊)


## 🚀 Getting Started

1. Copy `.env.example` to `.env` and tweak values if needed.
2. Start the stack with Docker Compose:

   ```bash
   docker-compose up --build
   ```

The Django app will connect to the bundled Postgres service using the
values from your `.env` file.

### Authentication Flow

1. Submit your login credentials to `/api/login/`.
2. The response body contains an `access` token and the `refresh` token is set
   in an **HttpOnly** cookie.
3. Store the access token only in memory and send it in the
   `Authorization: Bearer <token>` header for API calls.
4. When the access token expires, call `/api/token/refresh/` to obtain a new
   one. The backend reads the refresh token from the cookie.

## 🤝 Contributing

Contributions are super welcome — this project is being built in public, and I’d love help from fellow devs, designers, or collectors who want to make something cool for the PH Pokémon TCG scene.
Please read `CONTRIBUTING.md` for more details

### Ways You Can Help
This project is being built with the Filipino TCG community in mind — and there’s plenty of room for collaboration. Whether you're a coder, collector, or just curious, here’s how you can get involved:

 - Give Feedback – Found a bug? Got a feature idea? Open an issue or drop a comment.

 - Test Things Out – Try the app early, play around, and tell me what’s confusing or broken.

 - Contribute Code – If you know Django, HTMX, or Python, feel free to open a PR. Even small fixes help a lot.

 - Share With Others – Know fellow Pinoy collectors? Let them know this exists!

 - Suggest Cards/Features – Want a certain set or price tracker shown better? Tell me what you'd love to see.

 - Jam With Me – If you’re working on something similar or want to co-build, let’s talk.

I’m building this out in the open — no pressure, no hype, just honest progress. If it helps you or inspires you, that’s already a win.


### How to Contribute

1. ⭐ Star the repo to support the project!
2. 🐛 Check open [Issues](../../issues) or create one
3. 🍴 Fork the repo, create a branch, and open a PR
4. 📢 Share with friends or local groups

> If you're new to contributing, feel free to open a “draft” PR or issue — I’ll help guide you through it!

## 🌱 Community

This is a build-in-public project — you can follow progress, give feedback, or just lurk:

- 📓 See progress in [`CHANGELOG.md`](./CHANGELOG.md)
- 🐣 Say hi on Discord: `chizz902#9538`
- 💬 Reddit thread coming soon under [`u/chiz902`](https://www.reddit.com/user/chiz902/)
- 💌 Email: `hello@aimagineers.io`

## 📄 License

This project is open source under the **MIT License** — feel free to fork, use, remix, or build on top of it.
If you end up using this in your own work (or business), I’d love to hear about it!

---

### 🛠 From the same folks who build real impact

I run a studio called [AImagineers](check us out https://aimagineers.io) — where we build AI-powered systems, custom tools, and long-term tech for people solving real problems.
While this project started as a hobby, it’ll be powered by the same principles we use in our studio work: build slow, build right, security, and build things that matter.
