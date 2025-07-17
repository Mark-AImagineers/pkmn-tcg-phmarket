# 🤝 Contributing to Pokémon TCG Market PH

Hey there! 👋

First off — thank you for checking out this project. Whether you're here to report a bug, suggest a feature, write code, or just lurk around, you're more than welcome.

**Pokémon TCG Market PH** is a personal passion project being built in public, with a focus on helping Filipino collectors and players easily catalogue, trade, and sell cards. I’m a solo developer (for now), so I truly appreciate every bit of help.

> I'm not trying to build something perfect — just something that works, evolves, and helps our community. If you're here to make it better, you're already part of that mission.

---

## 🧠 Before You Start

- This project is work-in-progress. Some things might be half-built, break, or get changed along the way.
- Please read the README to understand the goals and design principles.
- Testing is early-stage. We're using `pytest` — and you’re welcome to improve coverage.
- Unsure about something? Open an issue or start a draft PR. Let’s talk first.

---

## 🛠 How to Contribute

1. **Fork the Repository**  
2. **Clone Your Fork**

    ```bash
    git clone https://github.com/your-username/pokemon-tcg-market-ph.git
    cd pokemon-tcg-market-ph
    ```

3. **Create a New Branch**

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**  
5. **Commit & Push**

    ```bash
    git add .
    git commit -m "feat: short description"
    git push origin feature/your-feature-name
    ```

6. **Open a Pull Request**

---

## 🧱 Project Folder Structure

Feature-based monolith with scalable config and deployment infra.

```text
pokemon_tcg_market_ph/
├── cards/
│   ├── models/
│   ├── views/
│   ├── api/
│   ├── services/
│   └── templates/cards/
├── collection/
├── marketplace/
├── trust/
├── templates/
├── static/
├── tests/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       ├── staging.py
│       └── production.py
├── docker/
│   ├── dev/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── prod/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
├── heroku/
│   ├── Procfile
│   ├── runtime.txt
│   └── app.json
├── .env
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── CHANGELOG.md
├── requirements.txt
└── version.json
```


---

## 🧼 Code Style

- Format code with **Black** (`black .`)
- Follow **PEP8**
- Use **docstrings** and inline comments where necessary
- Keep logic in `services/`, not inside views or serializers

---

## ✅ Commit Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org):

feat: add feature
fix: patch bug
refactor: restructure logic
docs: update documentation


---

## 🧪 Running Tests

Use `pytest`:

```bash
pytest
```

Each feature has its own folder under tests/.

### 🐞 Reporting Issues
If you run into bugs, ideas, or confusion:

```text
Use a clear title
Describe what you expected vs. what happened
Add screenshots or reproduction steps if helpful
```

🙏 Thank You
Every contribution helps — whether you're coding, testing, giving feedback, or sharing this with a friend. Let’s build something great for the Filipino Pokémon TCG community. Together.