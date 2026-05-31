from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Budget


# ---------------------------------------------------------------------------
# Budget views — Person 2
# ---------------------------------------------------------------------------

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'

    # TODO (Person 2): Override get_queryset to filter by:
    #   - user=request.user
    #   - month__year=today.year, month__month=today.month
    #
    # TODO (Person 2): Override get_context_data to annotate each budget with:
    #   - budget.spent — sum of Entry amounts for that category this month
    #     (filter: user, category, entry_type='EXPENSE', date__year, date__month)
    #   - budget.percentage — int((spent / budget.amount) * 100)
    #   - If percentage >= 80, emit a messages.warning() via Django messages framework


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')

    # TODO (Person 2): Set form_class = BudgetForm
    # TODO (Person 2): Override get_form_kwargs to pass user=request.user


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')

    # TODO (Person 2): Set form_class = BudgetForm
    # TODO (Person 2): Override get_queryset to filter by user=request.user
    # TODO (Person 2): Override get_form_kwargs to pass user=request.user


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

    # TODO (Person 2): Override get_queryset to filter by user=request.user
