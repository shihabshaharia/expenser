from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# ---------------------------------------------------------------------------
# Report views — Person 3
# ---------------------------------------------------------------------------

class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/report.html'

    # TODO (Person 3): Implement get_date_range(self) → (date_from, date_to)
    #   Read self.request.GET for:
    #     - 'preset' key: this_week | this_month | last_month | this_year |
    #                     last_year | tax_year
    #     - 'date_from' / 'date_to' for custom range
    #   Tax year logic (UK): start = April 6 current year if today >= April 6,
    #                        else April 6 previous year
    #   Default to 'this_month' if nothing is supplied

    # TODO (Person 3): Override get_context_data to add:
    #   date_from, date_to, preset
    #   total_income   — Sum of INCOME entries in range
    #   total_expenses — Sum of EXPENSE entries in range
    #   net_balance    — income - expenses
    #   by_category    — .values('category__name').annotate(total=Sum('amount'))
    #                    filtered to EXPENSE, ordered by -total
    #   top_5_expense_categories — by_category[:5]  (used for the Chart.js bar chart)
    #
    #   Use: Entry.objects.filter(user=user, date__gte=from, date__lte=to, is_recurring=False)
    #   Aggregate with Q objects: Sum('amount', filter=Q(entry_type='INCOME'))


class ExportCSVView(LoginRequiredMixin, TemplateView):
    # TODO (Person 3): Override get(self, request, ...) — do NOT use TemplateView.get
    #   1. Read date_from / date_to from request.GET
    #   2. Query entries for request.user in that range, select_related + prefetch_related tags
    #   3. Return HttpResponse(content_type='text/csv') with:
    #      Content-Disposition: attachment; filename="expenser_<from>_<to>.csv"
    #   4. Write CSV rows using Python's csv module:
    #      Header: Date, Type, Category, Amount, Description, Tags
    #      Tags column: comma-joined tag names
    #
    # Imports you will need:
    #   import csv
    #   from django.http import HttpResponse
    #   from core.models import Entry
    pass
