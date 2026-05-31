# Expenser — UI Design Guide

This document is the single source of truth for how every page and component in Expenser
should look. Copy the Tailwind class strings exactly — do not invent new colours or styles.
Everything here maps directly to the references shared with the team.

---

## 1. Design principles (from the references)

| Principle | What it means in practice |
|---|---|
| **White space over decoration** | Never add a border or background just to fill space — use padding and margin instead |
| **Semantic colour** | Green = income / success / positive. Red = expense / error / danger. Black = primary action. |
| **Thin, not heavy** | Borders are always `border-gray-200`, never thick or coloured |
| **Numbers are the star** | Stat values are large and bold; labels are small and muted |
| **Pills for status** | INCOME / EXPENSE / Active / Error are always small pill badges, never plain text |

---

## 2. Colour palette

Do not use any colour outside this list. All colours are standard Tailwind utility classes.

### Backgrounds
| Token | Tailwind class | When to use |
|---|---|---|
| Page background | `bg-white` | Every page |
| Card / surface | `bg-white` | Cards, panels, table rows |
| Muted surface | `bg-gray-50` | Table header row, filter bar, disabled inputs |
| Input background | `bg-white` | All form fields |

### Text
| Token | Tailwind class | When to use |
|---|---|---|
| Primary text | `text-gray-900` | Headings, values, important labels |
| Secondary text | `text-gray-500` | Card labels, helper text, placeholders |
| Muted text | `text-gray-400` | Timestamps, metadata |
| Link / action text | `text-gray-900 hover:text-gray-600` | Inline links |

### Semantic colours
| Token | Tailwind class | When to use |
|---|---|---|
| Income / success value | `text-green-600` | Income amounts, net positive balance, Active badge text |
| Expense / danger value | `text-red-600` | Expense amounts, negative balance, Error badge text |
| Warning value | `text-amber-600` | Budget near limit (80–99%) |
| Neutral stat | `text-gray-900` | Count values (number of entries, etc.) |

### Badge / pill backgrounds
| Badge | Background | Text |
|---|---|---|
| INCOME / Active | `bg-green-100` | `text-green-700` |
| EXPENSE / Error | `bg-red-100` | `text-red-700` |
| Warning | `bg-amber-100` | `text-amber-700` |
| Neutral tag | `bg-gray-100` | `text-gray-600` |

### Buttons
| Button type | Classes |
|---|---|
| Primary (black) | `bg-gray-900 text-white hover:bg-gray-700 rounded-lg px-4 py-2 text-sm font-medium` |
| Destructive (red) | `bg-red-600 text-white hover:bg-red-700 rounded-lg px-4 py-2 text-sm font-medium` |
| Ghost / secondary | `text-gray-500 hover:text-gray-900 px-4 py-2 text-sm font-medium` |
| Outline | `border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-lg px-4 py-2 text-sm font-medium` |

### Progress bar colours
| State | Bar class |
|---|---|
| Normal (< 80%) | `bg-green-500` |
| Warning (80–99%) | `bg-amber-400` |
| Over budget (≥ 100%) | `bg-red-500` |
| Track (background) | `bg-gray-200` |

---

## 3. Typography

Use the browser's default system font stack (no custom font import needed — Tailwind's
default sans covers this). Do not use `font-serif` or `font-mono` in templates.

| Role | Classes | Example |
|---|---|---|
| Page title | `text-2xl font-bold text-gray-900` | "Dashboard", "Entries" |
| Section heading | `text-lg font-semibold text-gray-900` | "Recent entries", "Budget progress" |
| Eyebrow label | `text-xs font-medium tracking-widest uppercase text-gray-400` | "THIS MONTH", "INCOME" |
| Card stat value | `text-3xl font-bold` + semantic colour | £1,240.00 |
| Body text | `text-sm text-gray-700` | Descriptions, table cells |
| Muted / helper | `text-xs text-gray-500` | Timestamps, field hints |
| Placeholder | handled by Tailwind's `placeholder:text-gray-400` on inputs | — |

---

## 4. Spacing and layout

### Page wrapper
Every page inside `base.html` already has this wrapper — do not add extra outer padding:
```html
<main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
```

### Content sections
Separate major sections with `mb-8` between them. Inside a section use `space-y-4` or
`space-y-6` on the container.

### Grid for stat cards (4-up)
```html
<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
```

### Two-column layout (content + sidebar)
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <div class="lg:col-span-2"> <!-- main content --> </div>
  <div>                        <!-- sidebar -->      </div>
</div>
```

---

## 5. Component library

Copy these HTML blocks directly into templates. Every class is intentional.

---

### 5.1 Page header

```html
<div class="flex items-center justify-between mb-6">
  <div>
    <p class="text-xs font-medium tracking-widest uppercase text-gray-400">May 2026</p>
    <h1 class="text-2xl font-bold text-gray-900 mt-0.5">Dashboard</h1>
  </div>
  <a href="{% url 'entry_create' %}"
     class="bg-gray-900 text-white hover:bg-gray-700 rounded-lg px-4 py-2 text-sm font-medium">
    + Add entry
  </a>
</div>
```

---

### 5.2 Stat card (for dashboard summary row)

```html
<!-- One card — repeat inside a 4-column grid -->
<div class="bg-white border border-gray-200 rounded-xl p-6">
  <p class="text-xs font-medium tracking-widest uppercase text-gray-400">Income this month</p>
  <p class="mt-4 text-3xl font-bold text-green-600">£1,240.00</p>
</div>
```

For the three dashboard cards use these colours:
- Income → `text-green-600`
- Expenses → `text-red-600`
- Net balance → `text-green-600` if positive, `text-red-600` if negative (use Django `{% if %}`)

```html
<!-- Dynamic colour example -->
<p class="mt-4 text-3xl font-bold {% if net_balance >= 0 %}text-green-600{% else %}text-red-600{% endif %}">
  £{{ net_balance }}
</p>
```

---

### 5.3 Status / type badge (pill)

```html
<!-- INCOME -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
  Income
</span>

<!-- EXPENSE -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
  Expense
</span>

<!-- Neutral tag -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
  {{ tag.name }}
</span>
```

Django tip — render the badge colour dynamically:
```html
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
  {% if entry.entry_type == 'INCOME' %}bg-green-100 text-green-700{% else %}bg-red-100 text-red-700{% endif %}">
  {{ entry.get_entry_type_display }}
</span>
```

---

### 5.4 Data table

```html
<div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
  <table class="min-w-full">
    <thead>
      <tr class="bg-gray-50 border-b border-gray-200">
        <th class="px-6 py-3 text-left text-xs font-medium tracking-widest uppercase text-gray-400">Date</th>
        <th class="px-6 py-3 text-left text-xs font-medium tracking-widest uppercase text-gray-400">Type</th>
        <th class="px-6 py-3 text-left text-xs font-medium tracking-widest uppercase text-gray-400">Category</th>
        <th class="px-6 py-3 text-right text-xs font-medium tracking-widest uppercase text-gray-400">Amount</th>
        <th class="px-6 py-3"></th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-100">
      {% for entry in entries %}
      <tr class="hover:bg-gray-50 transition-colors">
        <td class="px-6 py-4 text-sm text-gray-500">{{ entry.date }}</td>
        <td class="px-6 py-4">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
            {% if entry.entry_type == 'INCOME' %}bg-green-100 text-green-700{% else %}bg-red-100 text-red-700{% endif %}">
            {{ entry.get_entry_type_display }}
          </span>
        </td>
        <td class="px-6 py-4 text-sm text-gray-900">{{ entry.category.name }}</td>
        <td class="px-6 py-4 text-sm font-semibold text-right
          {% if entry.entry_type == 'INCOME' %}text-green-600{% else %}text-red-600{% endif %}">
          {% if entry.entry_type == 'INCOME' %}+{% else %}-{% endif %}£{{ entry.amount }}
        </td>
        <td class="px-6 py-4 text-right text-sm space-x-3">
          <a href="{% url 'entry_update' entry.pk %}" class="text-gray-400 hover:text-gray-900">Edit</a>
          <a href="{% url 'entry_delete' entry.pk %}" class="text-gray-400 hover:text-red-600">Delete</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5" class="px-6 py-12 text-center text-sm text-gray-400">
          No entries yet.
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

---

### 5.5 Form card (for Add / Edit pages)

Wrap every form page in this card:

```html
<div class="max-w-2xl">
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-gray-900">Add Entry</h1>
  </div>

  <div class="bg-white border border-gray-200 rounded-xl p-6">
    <form method="post" class="space-y-5">
      {% csrf_token %}

      <!-- Repeat this block for each field -->
      <div>
        <label for="{{ field.id_for_label }}"
               class="block text-sm font-medium text-gray-700 mb-1">
          {{ field.label }}
        </label>
        {{ field }}
        {% if field.help_text %}
          <p class="mt-1 text-xs text-gray-400">{{ field.help_text }}</p>
        {% endif %}
        {% if field.errors %}
          <p class="mt-1 text-xs text-red-600">{{ field.errors|join:", " }}</p>
        {% endif %}
      </div>

      {% if form.non_field_errors %}
        <div class="rounded-lg bg-red-50 border border-red-200 px-4 py-3">
          <p class="text-sm text-red-600">{{ form.non_field_errors|join:", " }}</p>
        </div>
      {% endif %}

      <div class="flex items-center gap-3 pt-2 border-t border-gray-100">
        <button type="submit"
                class="bg-gray-900 text-white hover:bg-gray-700 rounded-lg px-5 py-2 text-sm font-medium">
          Save
        </button>
        <a href="{% url 'entry_list' %}"
           class="text-sm text-gray-500 hover:text-gray-900 px-4 py-2">
          Cancel
        </a>
      </div>
    </form>
  </div>
</div>
```

### Form field styling — add to your form widgets

Django renders form fields as plain HTML inputs. To apply Tailwind classes, pass `attrs`
in each form's `__init__` or `Meta.widgets`. Here is the standard pattern to use:

```python
# In forms.py — inside __init__ or widgets dict
INPUT_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder:text-gray-400 '
    'focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent'
)

SELECT_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900'
)

TEXTAREA_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder:text-gray-400 '
    'focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none'
)
```

Apply them in `__init__`:
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
        widget = field.widget
        if hasattr(widget, 'input_type'):
            if widget.input_type in ('text', 'number', 'date', 'email', 'password'):
                widget.attrs['class'] = INPUT_CLASS
            elif widget.input_type == 'select':
                widget.attrs['class'] = SELECT_CLASS
        if widget.__class__.__name__ == 'Select':
            widget.attrs['class'] = SELECT_CLASS
        if widget.__class__.__name__ == 'Textarea':
            widget.attrs['class'] = TEXTAREA_CLASS
```

---

### 5.6 Filter bar (for entry list)

```html
<div class="bg-white border border-gray-200 rounded-xl p-4 mb-6">
  <form method="get" class="flex flex-wrap items-end gap-3">

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1">Type</label>
      <select name="entry_type"
              class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
        <option value="">All types</option>
        <option value="EXPENSE" {% if request.GET.entry_type == 'EXPENSE' %}selected{% endif %}>Expense</option>
        <option value="INCOME"  {% if request.GET.entry_type == 'INCOME'  %}selected{% endif %}>Income</option>
      </select>
    </div>

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1">Category</label>
      <select name="category"
              class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
        <option value="">All categories</option>
        {% for cat in categories %}
        <option value="{{ cat.pk }}" {% if request.GET.category == cat.pk|stringformat:"s" %}selected{% endif %}>
          {{ cat.name }}
        </option>
        {% endfor %}
      </select>
    </div>

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1">From</label>
      <input type="date" name="date_from" value="{{ request.GET.date_from }}"
             class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
    </div>

    <div>
      <label class="block text-xs font-medium text-gray-500 mb-1">To</label>
      <input type="date" name="date_to" value="{{ request.GET.date_to }}"
             class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
    </div>

    <button type="submit"
            class="bg-gray-900 text-white hover:bg-gray-700 rounded-lg px-4 py-1.5 text-sm font-medium">
      Filter
    </button>

    <a href="{{ request.path }}"
       class="text-sm text-gray-400 hover:text-gray-700 py-1.5">
      Clear
    </a>

  </form>
</div>
```

---

### 5.7 Budget progress card

```html
<!-- Repeat inside a space-y-4 container -->
<div class="bg-white border border-gray-200 rounded-xl p-5">
  <div class="flex items-center justify-between mb-3">
    <div>
      <p class="text-sm font-semibold text-gray-900">{{ budget.category.name }}</p>
      <p class="text-xs text-gray-400 mt-0.5">
        £{{ budget.spent }} spent of £{{ budget.amount }} limit
      </p>
    </div>
    <div class="flex items-center gap-3">
      <span class="text-sm font-semibold
        {% if budget.percentage >= 100 %}text-red-600
        {% elif budget.percentage >= 80 %}text-amber-600
        {% else %}text-gray-900{% endif %}">
        {{ budget.percentage }}%
      </span>
      <a href="{% url 'budget_update' budget.pk %}" class="text-xs text-gray-400 hover:text-gray-700">Edit</a>
      <a href="{% url 'budget_delete' budget.pk %}" class="text-xs text-gray-400 hover:text-red-600">Delete</a>
    </div>
  </div>

  <!-- Track -->
  <div class="w-full bg-gray-200 rounded-full h-1.5">
    <!-- Bar — cap width at 100% using template logic -->
    <div class="h-1.5 rounded-full transition-all duration-300
      {% if budget.percentage >= 100 %}bg-red-500
      {% elif budget.percentage >= 80 %}bg-amber-400
      {% else %}bg-green-500{% endif %}"
         style="width: {% if budget.percentage > 100 %}100{% else %}{{ budget.percentage }}{% endif %}%">
    </div>
  </div>
</div>
```

---

### 5.8 Empty state (for tables and lists with no data)

```html
<div class="text-center py-16">
  <p class="text-sm font-medium text-gray-900">No entries yet</p>
  <p class="text-xs text-gray-400 mt-1">Add your first entry to get started.</p>
  <a href="{% url 'entry_create' %}"
     class="mt-4 inline-block bg-gray-900 text-white hover:bg-gray-700 rounded-lg px-4 py-2 text-sm font-medium">
    + Add entry
  </a>
</div>
```

---

### 5.9 Delete confirmation page

```html
<div class="max-w-md">
  <h1 class="text-2xl font-bold text-gray-900 mb-2">Delete entry?</h1>
  <p class="text-sm text-gray-500 mb-6">
    This will permanently delete <strong class="text-gray-900">{{ object }}</strong>.
    This action cannot be undone.
  </p>
  <div class="bg-white border border-gray-200 rounded-xl p-6">
    <form method="post" class="flex items-center gap-3">
      {% csrf_token %}
      <button type="submit"
              class="bg-red-600 text-white hover:bg-red-700 rounded-lg px-5 py-2 text-sm font-medium">
        Yes, delete
      </button>
      <a href="{{ request.META.HTTP_REFERER|default:'/' }}"
         class="text-sm text-gray-500 hover:text-gray-900 px-4 py-2">
        Cancel
      </a>
    </form>
  </div>
</div>
```

---

### 5.10 Preset range tab bar (for reports page)

```html
{% with preset=request.GET.preset|default:'this_month' %}
<div class="flex flex-wrap gap-2 mb-6">
  {% for key, label in presets %}
  <a href="?preset={{ key }}"
     class="px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors
       {% if preset == key %}
         bg-gray-900 text-white border-gray-900
       {% else %}
         bg-white text-gray-600 border-gray-200 hover:border-gray-400 hover:text-gray-900
       {% endif %}">
    {{ label }}
  </a>
  {% endfor %}
</div>
{% endwith %}
```

In your `ReportView.get_context_data`, add this to pass the presets list to the template:
```python
ctx['presets'] = [
    ('this_week',  'This week'),
    ('this_month', 'This month'),
    ('last_month', 'Last month'),
    ('this_year',  'This year'),
    ('last_year',  'Last year'),
    ('tax_year',   'Tax year'),
]
```

---

### 5.11 Pagination controls

```html
{% if is_paginated %}
<div class="flex items-center justify-between mt-4 px-1">
  <p class="text-xs text-gray-400">
    Page {{ page_obj.number }} of {{ page_obj.num_pages }}
  </p>
  <div class="flex gap-2">
    {% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}"
       class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg text-gray-600 hover:border-gray-400">
      Previous
    </a>
    {% endif %}
    {% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}"
       class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg text-gray-600 hover:border-gray-400">
      Next
    </a>
    {% endif %}
  </div>
</div>
{% endif %}
```

---

### 5.12 Flash messages (Django messages framework)

This is already in `base.html`. The classes to use per level:

| Django level | Classes |
|---|---|
| `success` | `bg-green-50 border border-green-200 text-green-800` |
| `warning` | `bg-amber-50 border border-amber-200 text-amber-800` |
| `error` | `bg-red-50 border border-red-200 text-red-800` |
| `info` | `bg-blue-50 border border-blue-200 text-blue-800` |

Update the messages block in `base.html` to:
```html
{% if messages %}
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-4 space-y-2">
  {% for message in messages %}
  <div class="flex items-center justify-between rounded-lg px-4 py-3 text-sm
    {% if message.tags == 'success' %}bg-green-50 border border-green-200 text-green-800
    {% elif message.tags == 'warning' %}bg-amber-50 border border-amber-200 text-amber-800
    {% elif message.tags == 'error' %}bg-red-50 border border-red-200 text-red-800
    {% else %}bg-blue-50 border border-blue-200 text-blue-800{% endif %}">
    <span>{{ message }}</span>
  </div>
  {% endfor %}
</div>
{% endif %}
```

---

### 5.13 Auth pages (login / register)

Both pages use the same centred card layout:

```html
{% extends "base.html" %}
{% block content %}
<div class="min-h-[80vh] flex items-center justify-center">
  <div class="w-full max-w-sm">

    <!-- Logo / app name -->
    <div class="text-center mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Expenser</h1>
      <p class="text-sm text-gray-400 mt-1">Sign in to your account</p>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl px-6 py-8">
      <form method="post" class="space-y-4">
        {% csrf_token %}
        {% for field in form %}
        <div>
          <label for="{{ field.id_for_label }}"
                 class="block text-sm font-medium text-gray-700 mb-1">
            {{ field.label }}
          </label>
          {{ field }}
          {% if field.errors %}
            <p class="mt-1 text-xs text-red-600">{{ field.errors|join:", " }}</p>
          {% endif %}
        </div>
        {% endfor %}

        <button type="submit"
                class="w-full bg-gray-900 text-white hover:bg-gray-700 rounded-lg py-2.5 text-sm font-medium mt-2">
          Sign in
        </button>
      </form>

      <p class="mt-4 text-center text-xs text-gray-400">
        No account? <a href="{% url 'register' %}" class="text-gray-900 font-medium hover:underline">Register</a>
      </p>
    </div>

  </div>
</div>
{% endblock %}
```

---

## 6. Navigation bar

Update `base.html` to use this nav. It replaces the current indigo-coloured nav with a
clean minimal white top bar matching the references.

```html
<nav class="bg-white border-b border-gray-200">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex h-14 items-center justify-between">

      <!-- Left: logo + nav links -->
      <div class="flex items-center gap-8">
        <a href="{% url 'dashboard' %}"
           class="text-sm font-bold text-gray-900 tracking-tight">
          Expenser
        </a>
        {% if user.is_authenticated %}
        <div class="flex items-center gap-6">
          <a href="{% url 'dashboard' %}"
             class="text-sm text-gray-500 hover:text-gray-900 {% if request.resolver_match.url_name == 'dashboard' %}text-gray-900 font-medium{% endif %}">
            Dashboard
          </a>
          <a href="{% url 'entry_list' %}"
             class="text-sm text-gray-500 hover:text-gray-900 {% if 'entry' in request.resolver_match.url_name %}text-gray-900 font-medium{% endif %}">
            Entries
          </a>
          <a href="{% url 'category_list' %}"
             class="text-sm text-gray-500 hover:text-gray-900">
            Categories
          </a>
          <a href="{% url 'budget_list' %}"
             class="text-sm text-gray-500 hover:text-gray-900">
            Budgets
          </a>
          <a href="{% url 'report' %}"
             class="text-sm text-gray-500 hover:text-gray-900">
            Reports
          </a>
        </div>
        {% endif %}
      </div>

      <!-- Right: user + logout -->
      {% if user.is_authenticated %}
      <div class="flex items-center gap-4">
        <span class="text-xs text-gray-400">{{ user.username }}</span>
        <form method="post" action="{% url 'logout' %}">
          {% csrf_token %}
          <button type="submit"
                  class="text-xs text-gray-400 hover:text-gray-900">
            Log out
          </button>
        </form>
      </div>
      {% endif %}

    </div>
  </div>
</nav>
```

---

## 7. Chart.js setup (for the reports page)

Load Chart.js from CDN inside `{% block extra_js %}` at the bottom of `report.html`.
Use this exact config for a bar chart matching the reference aesthetic (no grid lines,
minimal labels, indigo bars):

```html
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const labels = [
    {% for row in top_5_expense_categories %}
      "{{ row.category__name }}"{% if not forloop.last %},{% endif %}
    {% endfor %}
  ];
  const values = [
    {% for row in top_5_expense_categories %}
      {{ row.total }}{% if not forloop.last %},{% endif %}
    {% endfor %}
  ];

  new Chart(document.getElementById('expenseChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Expenses (£)',
        data: values,
        backgroundColor: 'rgba(17, 24, 39, 0.85)',   /* gray-900 */
        borderRadius: 4,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ' £' + Number(ctx.raw).toFixed(2),
          },
        },
      },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: {
          grid: { color: '#F3F4F6' },
          border: { display: false },
          ticks: { callback: val => '£' + val },
        },
      },
    },
  });
</script>
{% endblock %}
```

In the template, add the canvas element inside your report card:
```html
<canvas id="expenseChart" class="w-full" height="280"></canvas>
```

---

## 8. Page-by-page checklist

Use this as a build checklist. Each page is listed with the components it needs.

| Page | Components to use |
|---|---|
| **Login** | Auth card (5.13) — update `login.html` |
| **Register** | Auth card (5.13) — update `register.html` |
| **Dashboard** | Page header (5.1) · Stat cards ×3 (5.2) · Budget progress cards (5.7) · Recent entries table (5.4, condensed) · Quick-add form (5.5) |
| **Entry list** | Page header (5.1) · Filter bar (5.6) · Data table (5.4) · Pagination (5.11) · Empty state (5.8) |
| **Entry add/edit** | Page header (5.1) · Form card (5.5) |
| **Entry delete** | Delete confirmation (5.9) |
| **Category list** | Page header (5.1) · Data table (5.4, simplified) · Empty state (5.8) |
| **Category add/edit** | Page header (5.1) · Form card (5.5) |
| **Category delete** | Delete confirmation (5.9) |
| **Budget list** | Page header (5.1) · Budget progress cards (5.7) · Empty state (5.8) |
| **Budget add/edit** | Page header (5.1) · Form card (5.5) |
| **Budget delete** | Delete confirmation (5.9) |
| **Reports** | Page header (5.1) · Preset tab bar (5.10) · Stat cards ×3 (5.2) · Data table for by-category (5.4) · Chart.js canvas (7) · CSV link |

---

## 9. Things NOT to do

- Do not use `bg-indigo-*` — the original scaffold used indigo but the design direction is monochrome (black/white/gray + semantic green/red)
- Do not add box shadows (`shadow-lg`, etc.) — borders do the job
- Do not use coloured nav bars — the nav is white with a bottom border only
- Do not add icons unless they are inline SVG or a simple Unicode character — no icon library is installed
- Do not write inline `style=""` attributes except for the progress bar width (which must be dynamic)
- Do not make the max content width wider than `max-w-7xl`
