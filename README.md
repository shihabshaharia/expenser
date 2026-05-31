# Expenser 💸

A personal finance management web application built with Django 5. Track daily income and expenses, categorise transactions, set budgets, log recurring entries, and generate reports — all using Django's built-in features.

> Built as a university project at Southeast University to demonstrate Django's core capabilities — ORM, class-based views, forms, signals, admin, template tags, and management commands.

---

## Features

- **Expense & income tracking** — log entries with amount, date, category, description, and tags
- **Categories** — create custom expense and income categories, seeded automatically on registration
- **Tags** — apply freeform labels to any entry for flexible filtering
- **Budgets** — set monthly spending limits per category with live progress and overspend warnings
- **Recurring entries** — flag transactions as recurring (daily / weekly / monthly / yearly) and auto-generate them via a management command
- **Reports** — generate summaries by week, month, year, tax year, or custom date range with charts
- **CSV export** — download any report as a CSV file using Python's built-in `csv` module
- **Django admin** — fully configured admin panel with filters, search, and date hierarchy
- **Built-in auth** — register, login, logout, password change and reset — all via `django.contrib.auth`

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2.1 |
| Database | PostgreSQL 16 |
| Styling | Tailwind CSS via `django-tailwind` 3.8.0 |
| Charts | Chart.js (CDN) |
| Containerisation | Docker + Docker Compose (optional) |
| Node.js | Node.js 20 LTS — required by `django-tailwind` for the Tailwind build pipeline |

---

## Getting started

Two setup paths are available — Docker (recommended, no manual config) or directly on a Ubuntu VM.

---

### Option A — Docker (recommended)

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

#### Steps

```bash
# 1. Clone the repo
git clone https://github.com/your-username/expenser.git
cd expenser

# 2. Copy environment file
cp .env.example .env

# 3. Build and start containers
docker compose up --build

# 4. In a new terminal — run migrations
docker compose exec web python manage.py migrate

# 5. Seed default categories
docker compose exec web python manage.py seed_categories

# 6. Create a superuser
docker compose exec web python manage.py createsuperuser

# 7. Start the Tailwind watcher
docker compose exec web python manage.py tailwind start
```

App runs at **http://localhost:8000** — admin at **http://localhost:8000/admin**

---

### Option B — Ubuntu VM (without Docker)

For teammates running the project directly on a Ubuntu 24.04 VM.


#### Prerequisites

- Ubuntu 24.04 LTS VM
- Internet access from inside the VM

#### Quick steps

```bash
# 1. Install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3.12 python3.12-venv python3-pip postgresql postgresql-contrib nodejs npm git -y

# 2. Start PostgreSQL
sudo systemctl start postgresql && sudo systemctl enable postgresql

# 3. Create database and user
sudo -u postgres psql -c "CREATE DATABASE expenser_db;"
sudo -u postgres psql -c "CREATE USER expenser_user WITH PASSWORD 'StrongPass123!';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE expenser_db TO expenser_user;"
sudo -u postgres psql -c "ALTER DATABASE expenser_db OWNER TO expenser_user;"

# 4. Clone and enter the repo
git clone https://github.com/your-username/expenser.git
cd expenser

# 5. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Configure environment — set DB_HOST=localhost
cp .env.example .env
nano .env

# 8. Run migrations and seed
python manage.py migrate
python manage.py seed_categories

# 9. Set up Tailwind
python manage.py tailwind install
python manage.py tailwind build

# 10. Create superuser and run
python manage.py createsuperuser
python manage.py runserver
```

> **Important:** In `.env`, set `DB_HOST=localhost` — not `db`. The value `db` is the Docker container name and only works with Docker.

In a second terminal, start the Tailwind watcher:

```bash
source venv/bin/activate
python manage.py tailwind start
```

---

## Project structure

```
expenser/
├── expenser/           # Project settings, root URLs, wsgi
├── accounts/           # User registration and auth views
├── core/               # Entry, Category, Tag models and views
├── budgets/            # Budget model and views
├── reports/            # Report views and CSV export
├── theme/              # django-tailwind theme app
├── templates/          # Shared base templates and partials
├── .env.example        # Example environment variables
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## Management commands

| Command | Description |
|---|---|
| `python manage.py seed_categories` | Seeds default expense and income categories for all existing users |
| `python manage.py process_recurring` | Processes recurring entries and generates new instances (planned) |
| `python manage.py tailwind install` | Installs Node dependencies for Tailwind (run once) |
| `python manage.py tailwind start` | Starts Tailwind CSS watcher in development |
| `python manage.py tailwind build` | Compiles and purges CSS for production |

---

## Environment variables

| Variable | Default | Notes |
|---|---|---|
| `DJANGO_SECRET_KEY` | *(set in .env)* | Django secret key — change before deployment |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |
| `DB_NAME` | `expenser_db` | PostgreSQL database name |
| `DB_USER` | `expenser_user` | PostgreSQL username |
| `DB_PASSWORD` | `expenser_pass` | PostgreSQL password |
| `DB_HOST` | `db` | `db` for Docker, `localhost` for VM setup |
| `DB_PORT` | `5432` | Default PostgreSQL port |

---

## Development workflow

Every time you sit down to work:

```bash
# Activate venv (non-Docker only)
source venv/bin/activate

# Pull latest changes
git pull

# Apply any new migrations
python manage.py migrate

# Terminal 1 — Django
python manage.py runserver

# Terminal 2 — Tailwind
python manage.py tailwind start
```

### Database access (Docker)

```bash
docker compose exec db psql -U expenser_user -d expenser_db
```

### Running tests

```bash
# Docker
docker compose exec web python manage.py test

# VM
python manage.py test
```

---

## Django built-ins used

This project is built to showcase Django's built-in capabilities. Key features demonstrated:

| Feature | Where used |
|---|---|
| `AbstractUser`, `LoginView`, `LogoutView`, `PasswordChangeView` | `accounts` |
| `UserCreationForm`, `ModelForm`, custom `clean()` | `accounts`, `core` |
| `LoginRequiredMixin`, `UserPassesTestMixin` | all apps |
| `CreateView`, `UpdateView`, `DeleteView`, `ListView` | `core`, `budgets` |
| `ManyToManyField`, `choices`, `unique_together` | `core`, `budgets` |
| `post_save` signal | `accounts` (seed categories on register) |
| Management commands | `core` (`seed_categories`, `process_recurring`) |
| ORM `filter()`, `aggregate()`, `annotate()`, `Sum` | `reports`, `budgets` |
| Django messages framework | `budgets` (overspend warnings) |
| `HttpResponse` with `text/csv` content type | `reports` (CSV export) |
| `ModelAdmin`, `list_filter`, `search_fields`, `date_hierarchy` | `admin` |
| Custom template tags and filters | `core`, `reports` |

---

## Team

| Name | Role | Owns |
|---|---|---|
| Shihab Shaharia | Setup + Core | Project scaffold, models, admin, auth, Docker, system design |
| [Teammate 2] | Entry management + Budgets | Entry CRUD, filtering, budgets, recurring entries, dashboard |
| [Teammate 3] | Reports + UI | Reports, CSV export, Chart.js, template tags, documentation |

---

## Licence

This project is for academic purposes at Southeast University. Not licensed for commercial use.
