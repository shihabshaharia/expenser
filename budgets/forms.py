from django import forms
from core.models import Category
from .models import Budget


# ---------------------------------------------------------------------------
# Person 2: implement BudgetForm
# ---------------------------------------------------------------------------

class BudgetForm(forms.ModelForm):
    """Form for creating/editing a monthly budget for an expense category."""

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            # type="month" renders a native month picker (YYYY-MM)
            'month': forms.DateInput(attrs={'type': 'month'}),
        }

    # TODO (Person 2): Accept `user` kwarg in __init__ and store as self._user
    # TODO (Person 2): In __init__, filter category queryset to:
    #   Category.objects.filter(user=user, entry_type='EXPENSE')
    # TODO (Person 2): clean_amount — raise ValidationError if amount <= 0
    # TODO (Person 2): Override save(commit=True) to set instance.user = self._user
