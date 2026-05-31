from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, ListView, TemplateView, UpdateView,
)

from .models import Category, Entry


# ---------------------------------------------------------------------------
# Dashboard — Person 2
# ---------------------------------------------------------------------------

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    # TODO (Person 2): Override get_context_data to add:
    #   - total_income / total_expenses / net_balance for the current month
    #     using Entry.objects.filter(...).aggregate(Sum('amount'))
    #   - recent_entries: last 10 entries for request.user
    #   - budgets: Budget.objects.filter(user, month=this month)
    #   - entry_form: an EntryForm instance (for the quick-add widget)


# ---------------------------------------------------------------------------
# Entry CRUD — Person 2
# ---------------------------------------------------------------------------

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'core/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 25

    # TODO (Person 2): Override get_queryset() to:
    #   - Always filter by user=request.user
    #   - Read GET params: entry_type, category, tag, date_from, date_to
    #   - Apply each filter with .filter() chaining
    #
    # TODO (Person 2): Override get_context_data to pass:
    #   - categories (for the filter dropdown)
    #   - the current GET params (so the template can pre-fill filters)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'core/entry_form.html'
    success_url = reverse_lazy('entry_list')

    # TODO (Person 2): Set form_class = EntryForm
    # TODO (Person 2): Override get_form_kwargs to pass user=request.user
    # Note: EntryForm.save() must set instance.user = self._user before saving


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    template_name = 'core/entry_form.html'
    success_url = reverse_lazy('entry_list')

    # TODO (Person 2): Set form_class = EntryForm
    # TODO (Person 2): Override get_form_kwargs to pass user=request.user
    # TODO (Person 2): Implement test_func to check self.get_object().user == request.user


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'core/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')

    # TODO (Person 2): Implement test_func to check self.get_object().user == request.user


# ---------------------------------------------------------------------------
# Category management — Person 2
# ---------------------------------------------------------------------------

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'categories'

    # TODO (Person 2): Override get_queryset to filter by user=request.user


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'core/category_form.html'
    success_url = reverse_lazy('category_list')

    # TODO (Person 2): Set form_class = CategoryForm
    # TODO (Person 2): Override get_form_kwargs to pass user=request.user


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'core/category_form.html'
    success_url = reverse_lazy('category_list')

    # TODO (Person 2): Set form_class = CategoryForm
    # TODO (Person 2): Override get_queryset to filter by user=request.user
    # TODO (Person 2): Implement test_func to verify ownership


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'core/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    # TODO (Person 2): Override get_queryset to filter by user=request.user
