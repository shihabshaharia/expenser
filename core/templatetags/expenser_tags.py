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
        return f'£{value:,.2f}'
    except (TypeError, ValueError):
        return '£0.00'


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
