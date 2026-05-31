from .models import Category

DEFAULT_CATEGORIES = {
    'EXPENSE': [
        'Food & Drink',
        'Transport',
        'Housing',
        'Utilities',
        'Healthcare',
        'Entertainment',
        'Shopping',
        'Education',
        'Other Expense',
    ],
    'INCOME': [
        'Salary',
        'Freelance',
        'Gift',
        'Investment Return',
        'Other Income',
    ],
}


def seed_default_categories(user):
    for entry_type, names in DEFAULT_CATEGORIES.items():
        for name in names:
            Category.objects.get_or_create(
                user=user,
                name=name,
                entry_type=entry_type,
            )
