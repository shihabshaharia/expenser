from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, ListView, TemplateView, UpdateView,
)

from budgets.models import Budget
from .forms import CategoryForm, EntryForm
from .models import Category, Entry


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = date.today()

        # Month-to-date income, expenses, net balance
        base_qs = Entry.objects.filter(
            user=user,
            date__year=today.year,
            date__month=today.month,
        )
        total_income = (
            base_qs.filter(entry_type=Entry.INCOME)
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        total_expenses = (
            base_qs.filter(entry_type=Entry.EXPENSE)
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        net_balance = total_income - total_expenses

        # 10 most recent entries — prefetch tags to avoid N+1 with tag_pills
        recent_entries = (
            Entry.objects.filter(user=user)
            .select_related('category')
            .prefetch_related('tags')
            .order_by('-date', '-created_at')[:10]
        )

        # Budgets for this month with spending annotated
        budgets = self._annotate_budgets(user, today)

        ctx.update({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'recent_entries': recent_entries,
            'budgets': budgets,
            'entry_form': EntryForm(user=user),
        })
        return ctx

    @staticmethod
    def _annotate_budgets(user, today):
        """Return this month's budgets with .spent and .percentage attached."""
        budgets = list(
            Budget.objects.filter(
                user=user,
                month__year=today.year,
                month__month=today.month,
            ).select_related('category')
        )
        for budget in budgets:
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
        return budgets


# ---------------------------------------------------------------------------
# Entry CRUD
# ---------------------------------------------------------------------------

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'core/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 25

    def get_queryset(self):
        qs = (
            Entry.objects.filter(user=self.request.user)
            .select_related('category')
            .prefetch_related('tags')
        )
        p = self.request.GET

        if p.get('entry_type'):
            qs = qs.filter(entry_type=p['entry_type'])

        if p.get('category'):
            qs = qs.filter(category_id=p['category'])

        if p.get('tag'):
            qs = qs.filter(tags__name__iexact=p['tag'])

        if p.get('date_from'):
            qs = qs.filter(date__gte=p['date_from'])

        if p.get('date_to'):
            qs = qs.filter(date__lte=p['date_to'])

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(user=self.request.user)
        ctx['current_filters'] = self.request.GET
        return ctx


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'core/entry_form.html'
    success_url = reverse_lazy('entry_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'core/entry_form.html'
    success_url = reverse_lazy('entry_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'core/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ---------------------------------------------------------------------------
# Category management
# ---------------------------------------------------------------------------

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.get_object().user == self.request.user


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'core/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
