from datetime import date

from django import forms

from .models import Category, Entry, Tag


# ---------------------------------------------------------------------------
# CategoryForm
# ---------------------------------------------------------------------------

class CategoryForm(forms.ModelForm):
    """Form for creating/editing a user-owned Category."""

    class Meta:
        model = Category
        fields = ['name', 'entry_type', 'icon', 'colour']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self._user
        if commit:
            instance.save()
        return instance


# ---------------------------------------------------------------------------
# EntryForm
# ---------------------------------------------------------------------------

class EntryForm(forms.ModelForm):
    """Form for creating/editing an Entry, including M2M tag input."""

    tag_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'work, holiday'}),
        help_text='Comma-separated tags',
    )

    class Meta:
        model = Entry
        fields = [
            'entry_type', 'amount', 'category', 'date',
            'description', 'is_recurring', 'recurrence_frequency',
        ]
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

        # Limit category choices to the current user's categories only
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

        # Pre-populate tag_input when editing an existing entry
        if self.instance.pk:
            existing_tags = self.instance.tags.values_list('name', flat=True)
            self.initial['tag_input'] = ', '.join(existing_tags)

    # ---- field-level validation ---------------------------------------- #

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount

    def clean_date(self):
        entry_date = self.cleaned_data.get('date')
        if entry_date and entry_date > date.today():
            raise forms.ValidationError('Date cannot be in the future.')
        return entry_date

    # ---- cross-field validation ---------------------------------------- #

    def clean(self):
        cleaned = super().clean()
        entry_type = cleaned.get('entry_type')
        category = cleaned.get('category')
        is_recurring = cleaned.get('is_recurring')
        recurrence_frequency = cleaned.get('recurrence_frequency')

        # Category type must match entry type
        if category and entry_type and category.entry_type != entry_type:
            raise forms.ValidationError(
                f'The selected category is for '
                f'{category.get_entry_type_display()} entries, '
                f'but the entry type is {dict(Entry.ENTRY_TYPE_CHOICES).get(entry_type)}. '
                f'Please choose a matching category.'
            )

        # Recurrence frequency is required when is_recurring is True
        if is_recurring and not recurrence_frequency:
            self.add_error(
                'recurrence_frequency',
                'Please select a frequency for this recurring entry.',
            )

        return cleaned

    # ---- save with M2M tag handling ------------------------------------ #

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self._user

        if commit:
            instance.save()

            # Parse comma-separated tag_input into Tag objects
            tag_input = self.cleaned_data.get('tag_input', '')
            tag_names = [t.strip() for t in tag_input.split(',') if t.strip()]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(user=self._user, name=name)
                tags.append(tag)
            instance.tags.set(tags)

            # Required for M2M with commit=True
            self.save_m2m = lambda: None  # already handled above

        return instance
