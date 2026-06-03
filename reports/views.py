"""
reports/views.py
================
Person 3 — Report views.

Implements:
  - ReportView : date-range selection, ORM aggregation, Chart.js context
  - ExportCSVView : CSV download for any date range
"""

import csv
from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.models import Entry


# Preset label pairs shown in the report tab bar
PRESETS = [
    ('this_week',   'This week'),
    ('this_month',  'This month'),
    ('last_month',  'Last month'),
    ('this_year',   'This year'),
    ('last_year',   'Last year'),
    ('tax_year',    'Tax year'),
]


class ReportView(LoginRequiredMixin, TemplateView):
    """
    Renders the reports page with summary stats and a Chart.js bar chart.

    Date range is driven by a ``?preset=`` query param, falling back to
    custom ``?date_from=`` / ``?date_to=`` values, and defaulting to the
    current calendar month.
    """

    template_name = 'reports/report.html'

    # ------------------------------------------------------------------
    # Date range helpers
    # ------------------------------------------------------------------

    def get_date_range(self):
        """
        Parse GET params and return (date_from, date_to) as date objects.

        Preset keys
        -----------
        this_week   — Monday of the current week → today
        this_month  — 1st of this month → today          (default)
        last_month  — 1st → last day of the previous month
        this_year   — 1 Jan this year → today
        last_year   — 1 Jan → 31 Dec of the previous year
        tax_year    — UK: 6 Apr this year → today (or 6 Apr last year if
                      today is before 6 Apr)
        custom      — explicit date_from / date_to params
        """
        today = date.today()
        preset = self.request.GET.get('preset', 'this_month')

        if preset == 'this_week':
            # ISO week starts on Monday (weekday() == 0)
            monday = today - timedelta(days=today.weekday())
            return monday, today

        if preset == 'last_month':
            first_of_this = today.replace(day=1)
            last_of_prev = first_of_this - timedelta(days=1)
            return last_of_prev.replace(day=1), last_of_prev

        if preset == 'this_year':
            return today.replace(month=1, day=1), today

        if preset == 'last_year':
            return date(today.year - 1, 1, 1), date(today.year - 1, 12, 31)

        if preset == 'tax_year':
            # UK tax year runs 6 April → 5 April
            tax_start = date(today.year, 4, 6)
            if today >= tax_start:
                return tax_start, today
            return date(today.year - 1, 4, 6), today

        if preset == 'custom' or (
            self.request.GET.get('date_from') or self.request.GET.get('date_to')
        ):
            try:
                date_from = date.fromisoformat(
                    self.request.GET.get('date_from') or today.replace(day=1).isoformat()
                )
            except ValueError:
                date_from = today.replace(day=1)
            try:
                date_to = date.fromisoformat(
                    self.request.GET.get('date_to') or today.isoformat()
                )
            except ValueError:
                date_to = today
            return date_from, date_to

        # Default — this month
        return today.replace(day=1), today

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    def get_context_data(self, **kwargs):
        """
        Build full context for report.html.

        Context keys
        ------------
        date_from, date_to      — date objects for the selected range
        preset                  — active preset key (or 'custom')
        presets                 — list of (key, label) for the tab bar
        total_income            — Decimal sum of INCOME entries
        total_expenses          — Decimal sum of EXPENSE entries
        net_balance             — income − expenses
        by_category             — QuerySet: {'category__name', 'total'}
                                  EXPENSE only, ordered −total
        top_5_expense_categories — first 5 rows of by_category (list)
                                   used for the Chart.js bar chart
        """
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        preset = self.request.GET.get('preset', 'this_month')
        date_from, date_to = self.get_date_range()

        # Base queryset — user's non-recurring entries in range
        # Recurring templates are excluded; only actual spend/income entries count.
        qs = Entry.objects.filter(
            user=user,
            date__gte=date_from,
            date__lte=date_to,
            is_recurring=False,
        )

        # Single-pass aggregation using Q filters (avoids two DB round-trips)
        totals = qs.aggregate(
            total_income=Sum('amount', filter=Q(entry_type=Entry.INCOME)),
            total_expenses=Sum('amount', filter=Q(entry_type=Entry.EXPENSE)),
        )
        total_income = totals['total_income'] or 0
        total_expenses = totals['total_expenses'] or 0
        net_balance = total_income - total_expenses

        # Category breakdown — expenses only, largest first
        by_category = (
            qs.filter(entry_type=Entry.EXPENSE)
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        # Materialise top 5 into a plain list so Chart.js template code can
        # serialise it with the `escapejs` filter without double evaluation.
        top_5_expense_categories = list(by_category[:5])

        ctx.update({
            'date_from':                   date_from,
            'date_to':                     date_to,
            'preset':                      preset,
            'presets':                     PRESETS,
            'total_income':                total_income,
            'total_expenses':              total_expenses,
            'net_balance':                 net_balance,
            'by_category':                 by_category,
            'top_5_expense_categories':    top_5_expense_categories,
        })
        return ctx


# ---------------------------------------------------------------------------


class ExportCSVView(LoginRequiredMixin, TemplateView):
    """
    Stream a CSV file of entries for the selected date range.

    Query params
    ------------
    date_from  — ISO date string (YYYY-MM-DD); defaults to 1st of current month
    date_to    — ISO date string (YYYY-MM-DD); defaults to today

    Response
    --------
    Content-Type: text/csv
    Content-Disposition: attachment; filename="expenser_<from>_<to>.csv"

    Columns: Date, Type, Category, Amount, Description, Tags
    """

    def get(self, request, *args, **kwargs):
        today = date.today()

        # Parse date range from query string
        try:
            date_from = date.fromisoformat(
                request.GET.get('date_from') or today.replace(day=1).isoformat()
            )
        except ValueError:
            date_from = today.replace(day=1)

        try:
            date_to = date.fromisoformat(
                request.GET.get('date_to') or today.isoformat()
            )
        except ValueError:
            date_to = today

        # Fetch entries — select_related for single JOIN on category,
        # prefetch_related tags to avoid N+1 on the M2M
        entries = (
            Entry.objects.filter(
                user=request.user,
                date__gte=date_from,
                date__lte=date_to,
            )
            .select_related('category')
            .prefetch_related('tags')
            .order_by('-date', '-created_at')
        )

        # Build streaming CSV response
        filename = f'expenser_{date_from.isoformat()}_{date_to.isoformat()}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        # Header row
        writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description', 'Tags'])

        for entry in entries:
            # Tags column: comma-joined tag names
            tags_str = ', '.join(tag.name for tag in entry.tags.all())
            writer.writerow([
                entry.date.isoformat(),
                entry.get_entry_type_display(),
                entry.category.name,
                str(entry.amount),
                entry.description,
                tags_str,
            ])

        return response
