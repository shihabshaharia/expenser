from django import template

register = template.Library()

# ---------------------------------------------------------------------------
# Custom template tags & filters — Person 3
# ---------------------------------------------------------------------------

# TODO (Person 3): @register.inclusion_tag('core/partials/tag_pills.html')
# def tag_pills(entry):
#     """Render coloured pill badges for each tag on an entry."""
#     return {'tags': entry.tags.all()}
#
# Usage in templates: {% tag_pills entry %}
# Requires: templates/core/partials/tag_pills.html


# TODO (Person 3): @register.filter
# def currency(value):
#     """Format a Decimal as £1,234.56"""
#     return f'£{value:,.2f}'
#
# Usage in templates: {{ entry.amount|currency }}


# TODO (Person 3): @register.filter
# def percentage(value, total):
#     """Return int percentage of value/total, capped at 100."""
#     if not total:
#         return 0
#     return min(int((value / total) * 100), 100)
#
# Usage in templates: {{ budget.spent|percentage:budget.amount }}
