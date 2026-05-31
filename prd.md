# Expenser — Product Requirements Document

**Version:** 1.0  
**Date:** May 2026  
**Team:** 3-person university project  
**Course:** Southeast University  
**Status:** Draft

---

## 1. Overview

### 1.1 Project summary

Expenser is a personal finance management web application built with Django. It allows users to track their daily income and expenses, organise entries by category and tags, set monthly budgets per category, log recurring transactions, and generate reports over flexible date ranges (weekly, monthly, yearly, tax year).

The primary goal of this project is to demonstrate Django's built-in capabilities — the ORM, class-based views, form handling, authentication system, signals, admin panel, template tags, and management commands — within a real, usable product.

### 1.2 Objectives

- Build a fully functional expense and income tracker using Django's built-in tools
- Demonstrate clean use of Django models, ORM queries, CBVs, and forms
- Implement Django's auth system for user isolation (each user sees only their own data)
- Produce readable, well-documented code suitable for academic submission
- Split work across three contributors with clearly defined ownership

### 1.3 Out of scope

- Mobile app or native client
- Django REST Framework / API-first architecture
- Social login (Google, GitHub, etc.)
- Multi-currency support
- Real-time notifications or WebSocket features
- Payment gateway integration

---

## 2. Users

### 2.1 Target user

A single authenticated user managing their own finances. There are no shared household or multi-user collaboration features in v1.

### 2.2 User roles

| Role | Description |
|---|---|
| Regular user | Can manage their own expenses, income, categories, tags, budgets, and reports |
| Admin (superuser) | Full Django admin access — can view/manage all users and their data |

All registered users are regular users by default. Admin is a Django superuser set via `createsuperuser`.

---

## 3. Features

### 3.1 Authentication (Django built-in)

- Register with username, email, and password — using Django's `UserCreationForm`
- Login / logout using `LoginView` and `LogoutView`
- Password change using `PasswordChangeView`
- Password reset via email using `PasswordResetView` and `PasswordResetConfirmView`
- All auth views from `django.contrib.auth` — no third-party packages

**Django built-ins showcased:** `AbstractUser`, `authenticate()`, `login()`, `logout()`, `@login_required`, `LoginRequiredMixin`

---

### 3.2 Categories

Users can create and manage their own expense/income categories.

**Attributes:**
- Name (e.g. Food, Transport, Salary)
- Type: `EXPENSE` or `INCOME`
- Icon / colour (optional cosmetic field — stored as a string slug)
- Created by (FK to user — users only see their own categories)

**Defaults:** A set of default categories is seeded via a Django **management command** (`python manage.py seed_categories`) when a new user registers, using Django **signals** (`post_save` on `User`).

**Django built-ins showcased:** `ModelForm`, `CreateView`, `UpdateView`, `DeleteView`, `post_save` signal, management commands

---

### 3.3 Tags

Freeform labels that can be applied to any expense or income entry. Tags belong to the user.

**Attributes:**
- Name (e.g. `holiday`, `work`, `one-off`)
- Created by (FK to user)

Tags are entered as a comma-separated text input on the entry form and stored via a `ManyToManyField`. The template uses a custom **template tag** to render tag pills.

**Django built-ins showcased:** `ManyToManyField`, custom template tags

---

### 3.4 Expense & income entries

The core model. Each entry is either an expense or an income.

**Attributes:**

| Field | Type | Notes |
|---|---|---|
| `user` | FK → User | Owner |
| `entry_type` | CharField (choices) | `EXPENSE` or `INCOME` |
| `amount` | DecimalField | Positive, 2 decimal places |
| `category` | FK → Category | Must match `entry_type` |
| `tags` | M2M → Tag | Optional |
| `date` | DateField | Defaults to today |
| `description` | TextField | Optional notes |
| `is_recurring` | BooleanField | Flags recurring entries |
| `recurrence_frequency` | CharField (choices) | `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY` — null if not recurring |
| `created_at` | DateTimeField | Auto |
| `updated_at` | DateTimeField | Auto |

**Views:**
- List view with filter by type, category, tag, date range — using Django `ListView` + `get_queryset()` override
- Create / edit / delete via `CreateView`, `UpdateView`, `DeleteView`
- Quick-add form on the dashboard

**Django built-ins showcased:** `DecimalField`, `DateField`, `choices`, `ManyToManyField`, `get_queryset()`, `LoginRequiredMixin`, `UserPassesTestMixin`

---

### 3.5 Recurring entries

When `is_recurring = True`, the entry is a template. A Django **management command** (`python manage.py process_recurring`) reads all active recurring entries and creates new entry instances as needed based on `recurrence_frequency` and the last-processed date.

In development, this command is run manually. In production it would be scheduled (e.g. cron or Celery — out of scope for this project, but documented).

**Django built-ins showcased:** Management commands, ORM date filtering (`__gte`, `__lte`, `timedelta`)

---

### 3.6 Budgets

Users can set a monthly spending budget per category.

**Attributes:**

| Field | Type | Notes |
|---|---|---|
| `user` | FK → User | Owner |
| `category` | FK → Category | One budget per category |
| `amount` | DecimalField | Monthly limit |
| `month` | DateField | First day of the target month |

**Budget progress** is calculated on the fly in the view using Django ORM aggregation (`Sum`). A progress bar is rendered in the template showing current spend vs. budget limit.

If spending exceeds 80% of the budget, a warning is displayed using Django's **messages framework**.

**Django built-ins showcased:** `Sum` aggregation, `annotate()`, `messages` framework, `unique_together`

---

### 3.7 Reports

Users can generate summary reports for any date range.

**Preset ranges (via query params):**
- This week
- This month
- Last month
- This year
- Last year
- Tax year (April 6 – April 5, UK-style)
- Custom date range (from / to date picker)

**Report content:**
- Total income, total expenses, net balance for the period
- Breakdown by category (table + bar chart using Chart.js via a `<script>` tag — no Django plugin needed)
- Top 5 expense categories
- Month-by-month summary table (for yearly reports)
- Export to CSV using Python's built-in `csv` module via a Django view that returns `HttpResponse` with `content_type='text/csv'`

**Django built-ins showcased:** ORM `filter()` + `aggregate()` + `annotate()` + `values()`, `HttpResponse`, custom date range logic, template context processors

---

### 3.8 Dashboard

The landing page after login. Shows:
- Current month's total income, total expenses, net balance (cards)
- Budget progress bars for all active budgets this month
- Recent 10 entries (quick list)
- Quick-add expense / income form

All data is computed in the view using ORM queries — no raw SQL.

---

### 3.9 Django admin

The admin panel (`/admin/`) is configured to allow superusers to:
- View and filter all users' entries, categories, and budgets
- Use list filters for `entry_type`, `category`, `date`, `is_recurring`
- Search entries by description or tag name
- Use `list_display`, `list_filter`, `search_fields`, `date_hierarchy`

**Django built-ins showcased:** `ModelAdmin`, `list_display`, `list_filter`, `search_fields`, `date_hierarchy`, `readonly_fields`

---

## 4. System design

### 4.1 Architecture

```
Browser
  └── Django (MTV)
        ├── URLs          urls.py (per-app + project-level include())
        ├── Views         Class-based views (ListView, CreateView, etc.)
        ├── Templates     Django template engine + template tags
        ├── Forms         ModelForm + custom validation
        ├── Models        ORM (PostgreSQL)
        ├── Signals       post_save on User → seed categories
        ├── Admin         django.contrib.admin
        └── Management    seed_categories, process_recurring
```

### 4.2 Data model (ERD summary)

```
User (Django built-in AbstractUser)
 ├── Category (user FK, entry_type, name)
 ├── Tag (user FK, name)
 ├── Entry (user FK, category FK, tags M2M, amount, date, is_recurring, recurrence_frequency)
 └── Budget (user FK, category FK, amount, month)
```

Full ERD diagram is provided separately (see system design document).

### 4.3 URL structure

| URL | View | Description |
|---|---|---|
| `/` | `DashboardView` | Home / dashboard |
| `/accounts/register/` | `RegisterView` | User registration |
| `/accounts/login/` | `LoginView` (built-in) | Login |
| `/accounts/logout/` | `LogoutView` (built-in) | Logout |
| `/accounts/password-change/` | `PasswordChangeView` (built-in) | Change password |
| `/accounts/password-reset/` | `PasswordResetView` (built-in) | Reset password |
| `/entries/` | `EntryListView` | List + filter entries |
| `/entries/add/` | `EntryCreateView` | Add entry |
| `/entries/<pk>/edit/` | `EntryUpdateView` | Edit entry |
| `/entries/<pk>/delete/` | `EntryDeleteView` | Delete entry |
| `/categories/` | `CategoryListView` | Manage categories |
| `/categories/add/` | `CategoryCreateView` | Add category |
| `/budgets/` | `BudgetListView` | Manage budgets |
| `/budgets/add/` | `BudgetCreateView` | Add budget |
| `/reports/` | `ReportView` | Generate reports |
| `/reports/export/` | `ExportCSVView` | Download CSV |
| `/admin/` | Django admin | Admin panel |

### 4.4 Apps structure

```
expenser/                  ← Django project
├── expenser/              ← Project settings package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              ← User auth, registration
├── core/                  ← Entry, Category, Tag models + views
├── budgets/               ← Budget model + views
├── reports/               ← Report views + CSV export
├── templates/             ← Shared base templates
├── static/                ← CSS, JS (Chart.js CDN)
└── manage.py
```

### 4.5 Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.x |
| Database | PostgreSQL 16 (via Docker) |
| Frontend | Django templates + Tailwind CSS (via django-tailwind) |
| Charts | Chart.js (CDN) |
| Containerisation | Docker + Docker Compose |
| Python env | venv / requirements.txt |
| Node.js | Required by django-tailwind for the Tailwind build pipeline (installed in Docker container) |

### 4.6 Styling approach

Tailwind CSS is integrated via the `django-tailwind` package, which wraps the Tailwind build pipeline inside Django management commands. This keeps the workflow Django-native — no separate frontend tooling to manage.

**How it works:**
- `django-tailwind` is added to `INSTALLED_APPS` as `tailwind` plus a `theme` app it generates
- `python manage.py tailwind install` — installs Node dependencies (run once)
- `python manage.py tailwind start` — starts the Tailwind watcher in development (runs alongside `runserver`)
- `python manage.py tailwind build` — compiles and purges CSS for production
- `tailwind.config.js` is pre-configured to scan all Django templates automatically — unused classes are purged in production

**Docker:** Node.js is installed in the `web` container via the Dockerfile. Both `tailwind start` and `runserver` run together in development using a process manager or separate `docker compose` commands.

**Design approach:** Tailwind utility classes are used directly in Django templates. A shared `base.html` defines the layout shell. Component partials (cards, buttons, forms, tables) are extracted into `{% include %}` snippets for reuse across apps.

---

## 5. Team split

### Person 1 — Shihab (Setup + Core)

**Owns:**
- Docker setup and project scaffold (`django-admin startproject`, app creation, settings, URL routing)
- Django models for `Entry`, `Category`, `Tag` (the core data layer)
- User registration view (since auth is the entry point for everything)
- Django admin configuration for all models
- `seed_categories` management command + `post_save` signal
- Base templates, layout, Bootstrap integration
- System design documentation and ERD

**Why this split:** The setup and data model are the foundation everything else depends on. Shihab finishes first, unblocks the team.

---

### Person 2 — Entry management + Budgets

**Owns:**
- All `Entry` CRUD views (`EntryListView`, `EntryCreateView`, `EntryUpdateView`, `EntryDeleteView`)
- Entry list filtering (by type, category, date range, tag) using `get_queryset()`
- `Budget` model, views, and budget progress calculations using ORM aggregation
- Budget warning messages using Django's messages framework
- `process_recurring` management command
- Tag input UX (comma-separated input on entry form → M2M save)
- Dashboard quick-add form

**Why this split:** Entry management + budgets are tightly linked around the same data and views — one person owning this avoids merge conflicts.

---

### Person 3 — Reports + UI polish

**Owns:**
- `ReportView` — all date range logic, ORM aggregation queries, context building
- Chart.js integration (bar chart, category breakdown)
- CSV export view (`ExportCSVView`)
- Custom template tags (tag pill renderer, currency filter, percentage filter)
- Template polish — responsive layout, budget progress bars, dashboard cards
- Documentation (code comments, README, user guide)

**Why this split:** Reports require solid ORM knowledge and clean data visualisation. UI polish and template tags naturally pair with this.

---

## 6. Django built-ins showcase checklist

This table maps every major Django feature used in the project to the module that uses it — for easy marking reference.

| Django feature | Used in |
|---|---|
| `AbstractUser` / auth system | accounts |
| `LoginView`, `LogoutView`, `PasswordChangeView`, `PasswordResetView` | accounts |
| `UserCreationForm` | accounts |
| `@login_required` / `LoginRequiredMixin` | all apps |
| `UserPassesTestMixin` | core (entry ownership check) |
| `ModelForm` + custom `clean()` | core, budgets |
| `CreateView`, `UpdateView`, `DeleteView`, `ListView`, `TemplateView` | core, budgets, reports |
| `get_queryset()` override | core (filtering) |
| `ManyToManyField` | core (tags) |
| `post_save` signal | accounts (seed categories) |
| Management commands | core (`seed_categories`, `process_recurring`) |
| ORM `filter()`, `aggregate()`, `annotate()`, `values()` | reports, budgets |
| `Sum` aggregation | budgets, reports |
| Django messages framework | budgets (budget warnings) |
| `HttpResponse` with custom content type | reports (CSV export) |
| `ModelAdmin` with `list_display`, `list_filter`, `search_fields`, `date_hierarchy` | admin |
| Custom template tags and filters | core, reports |
| `unique_together` constraint | budgets |
| `choices` on model fields | core |

---

## 7. Non-functional requirements

- **Security:** All views behind `LoginRequiredMixin`. Entries are filtered by `request.user` in every queryset — no user can access another's data.
- **Data integrity:** `unique_together` on Budget(user, category, month). Category FK is protected to prevent deletion of categories with entries.
- **Validation:** All amounts must be positive. Entry date cannot be in the future (custom `clean()` on form). Category type must match entry type.
- **Code quality:** Each app has its own `urls.py`, `views.py`, `models.py`, `forms.py`, `admin.py`. No business logic in templates.

---

## 8. Milestones

| Week | Milestone |
|---|---|
| Week 1 | Docker up, project scaffold, models defined, migrations run, admin working |
| Week 2 | Entry CRUD + category management + auth complete |
| Week 3 | Budgets, recurring management command, dashboard |
| Week 4 | Reports, CSV export, Chart.js integration |
| Week 5 | Template polish, custom template tags, documentation |
| Week 6 | Final review, testing, submission prep |

---

## 9. Appendix

### 9.1 Suggested default categories

**Expense:** Food & Drink, Transport, Housing, Utilities, Healthcare, Entertainment, Shopping, Education, Other Expense

**Income:** Salary, Freelance, Gift, Investment Return, Other Income

These are seeded automatically on new user registration via the `post_save` signal + `seed_categories` management command.

### 9.2 Tax year definition

For the UK tax year (6 April – 5 April), the report view calculates:
- If current date is on or after April 6 → tax year start = April 6 of current year
- If current date is before April 6 → tax year start = April 6 of previous year

This is handled in pure Python in the `ReportView.get_date_range()` method.

### 9.3 CSV export format

```
Date,Type,Category,Amount,Description,Tags
2026-05-01,EXPENSE,Food & Drink,12.50,Lunch with team,"work,food"
2026-05-03,INCOME,Salary,50000.00,Monthly salary,""
```
