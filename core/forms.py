from django import forms
from .models import Category, Entry


# ---------------------------------------------------------------------------
# Person 2: implement both forms below
# ---------------------------------------------------------------------------

class CategoryForm(forms.ModelForm):
    """Form for creating/editing a user-owned Category."""

    class Meta:
        model = Category
        fields = ['name', 'entry_type', 'icon', 'colour']

    # TODO (Person 2): Accept `user` kwarg in __init__ and store as self._user
    # TODO (Person 2): Override save(commit=True) to set instance.user = self._user


class EntryForm(forms.ModelForm):
    """Form for creating/editing an Entry, including M2M tag input."""

    # TODO (Person 2): Add a `tag_input` CharField (comma-separated, not required)
    #   widget: TextInput with placeholder 'work, holiday'
    #   help_text: 'Comma-separated tags'

    class Meta:
        model = Entry
        fields = [
            'entry_type', 'amount', 'category', 'date',
            'description', 'is_recurring', 'recurrence_frequency',
        ]
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    # TODO (Person 2): Accept `user` kwarg in __init__ and store as self._user
    # TODO (Person 2): In __init__, filter category queryset to user's categories only
    # TODO (Person 2): In __init__, if editing (self.instance.pk), pre-populate tag_input

    # TODO (Person 2): clean_amount — raise ValidationError if amount <= 0
    # TODO (Person 2): clean_date — raise ValidationError if date > today
    # TODO (Person 2): clean — raise ValidationError if category.entry_type != entry_type
    #                         also validate recurrence_frequency required when is_recurring

    # TODO (Person 2): Override save(commit=True) to:
    #   1. Set instance.user = self._user
    #   2. Call instance.save()
    #   3. Parse tag_input, get_or_create each Tag, call instance.tags.set(tags)
