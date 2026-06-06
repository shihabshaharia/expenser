"""
core/templatetags/expenser_tags.py
===================================
Person 3 — Custom template tags and filters for the Expenser project.

Registered items
----------------
tag_pills(entry)        inclusion tag  — renders coloured pill badges for
                                         each tag attached to an entry
currency(value)         filter         — formats a Decimal as £1,234.56
percentage(value,total) filter         — int % of value/total, capped at 100

Usage examples
--------------
In any template that starts with {% load expenser_tags %}:

    {% tag_pills entry %}
    {{ entry.amount|currency }}
    {{ budget.spent|percentage:budget.amount }}
"""

from django import template

register = template.Library()

# Deterministic color palette for category avatars
_AVATAR_COLORS = [
    'bg-red-500',    'bg-purple-500', 'bg-teal-600',  'bg-blue-500',
    'bg-orange-500', 'bg-pink-500',   'bg-indigo-500','bg-emerald-600',
    'bg-amber-500',  'bg-cyan-600',   'bg-rose-500',  'bg-violet-600',
]

_AVATAR_HEX = [
    '#ef4444', '#a855f7', '#0d9488', '#3b82f6',
    '#f97316', '#ec4899', '#6366f1', '#059669',
    '#f59e0b', '#0891b2', '#f43f5e', '#7c3aed',
]

@register.filter(name='category_color')
def category_color(name):
    """Return a deterministic Tailwind bg class for a category name."""
    idx = sum(ord(c) for c in str(name)) % len(_AVATAR_COLORS)
    return _AVATAR_COLORS[idx]

@register.filter(name='category_color_hex')
def category_color_hex(name):
    """Return a deterministic hex color for a category name (for inline styles)."""
    idx = sum(ord(c) for c in str(name)) % len(_AVATAR_HEX)
    return _AVATAR_HEX[idx]


# ---------------------------------------------------------------------------
# Inclusion tag — tag pills
# ---------------------------------------------------------------------------

@register.inclusion_tag('core/partials/tag_pills.html')
def tag_pills(entry):
    """
    Render coloured pill badges for every tag attached to *entry*.

    Requires the partial template at:
        templates/core/partials/tag_pills.html

    Template receives a ``tags`` variable — a QuerySet of Tag objects.

    Example
    -------
    {% load expenser_tags %}
    {% tag_pills entry %}
    """
    return {'tags': entry.tags.all()}


# ---------------------------------------------------------------------------
# Filter — currency
# ---------------------------------------------------------------------------

@register.filter(name='currency')
def currency(value):
    """
    Format *value* as a GBP string, e.g. ``£1,234.56``.

    Handles None and non-numeric values gracefully by returning ``£0.00``.

    Example
    -------
    {{ entry.amount|currency }}   →   £42.50
    {{ total_expenses|currency }} →   £1,200.00
    """
    try:
        return f'৳{value:,.2f}'
    except (TypeError, ValueError):
        return '৳0.00'


# ---------------------------------------------------------------------------
# Filter — percentage
# ---------------------------------------------------------------------------

@register.filter(name='percentage')
def percentage(value, total):
    """
    Return the integer percentage of *value* out of *total*, capped at 100.

    Returns 0 when *total* is zero or None to prevent division errors.

    Example
    -------
    {{ budget.spent|percentage:budget.amount }}   →   73
    {{ 1200|percentage:1000 }}                    →   100  (capped)
    """
    try:
        if not total:
            return 0
        return min(int((value / total) * 100), 100)
    except (TypeError, ZeroDivisionError, ValueError):
        return 0
