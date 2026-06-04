from django import forms

from core.models import Category
from .models import Budget


class BudgetForm(forms.ModelForm):
    """Form for creating/editing a monthly budget for an expense category."""

    _INPUT_CLASS = (
        'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
        'text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900'
    )

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'category': forms.Select(attrs={'class': (
                'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
                'text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900'
            )}),
            'amount': forms.NumberInput(attrs={
                'class': (
                    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
                    'text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900'
                ),
                'step': '0.01', 'min': '0.01',
            }),
            # type="month" renders a native YYYY-MM month picker in the browser
            'month': forms.DateInput(attrs={
                'type': 'month',
                'class': (
                    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
                    'text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900'
                ),
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

        # Only show the user's EXPENSE categories (budgets track spending)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(
                user=user, entry_type=Category.EXPENSE
            )

        # Pre-format the month field value for the type="month" widget (YYYY-MM)
        if self.instance.pk and self.instance.month:
            self.initial['month'] = self.instance.month.strftime('%Y-%m')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Budget limit must be greater than zero.')
        return amount

    def clean_month(self):
        """
        The type="month" input submits "YYYY-MM". Django's DateField expects
        "YYYY-MM-DD", so we append "-01" to normalise to the first of the month.
        """
        month = self.cleaned_data.get('month')
        if month:
            # If Django already parsed it as a date object, just normalise the day
            import datetime
            if isinstance(month, datetime.date):
                return month.replace(day=1)
        return month

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self._user
        if commit:
            instance.save()
        return instance
