from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.models import Entry
from .forms import BudgetForm
from .models import Budget


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        today = date.today()
        return Budget.objects.filter(
            user=self.request.user,
            month__year=today.year,
            month__month=today.month,
        ).select_related('category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        user = self.request.user

        # Annotate each budget with ORM-aggregated spending + percentage
        for budget in ctx['budgets']:
            spent = (
                Entry.objects.filter(
                    user=user,
                    category=budget.category,
                    entry_type=Entry.EXPENSE,
                    date__year=today.year,
                    date__month=today.month,
                ).aggregate(total=Sum('amount'))['total'] or 0
            )
            budget.spent = spent
            budget.percentage = (
                int((spent / budget.amount) * 100) if budget.amount else 0
            )

            # Warn via Django messages framework when nearing / over budget
            if budget.percentage >= 100:
                messages.warning(
                    self.request,
                    f'⚠ You have exceeded your {budget.category.name} budget '
                    f'({budget.percentage}% used — £{spent} of £{budget.amount}).',
                )
            elif budget.percentage >= 80:
                messages.warning(
                    self.request,
                    f'⚠ You are approaching your {budget.category.name} budget '
                    f'({budget.percentage}% used — £{spent} of £{budget.amount}).',
                )

        return ctx


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BudgetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user


class BudgetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user
