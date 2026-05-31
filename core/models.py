from datetime import date
from django.conf import settings
from django.db import models


class Category(models.Model):
    EXPENSE = 'EXPENSE'
    INCOME = 'INCOME'
    TYPE_CHOICES = [(EXPENSE, 'Expense'), (INCOME, 'Income')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=100)
    entry_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True)
    colour = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['entry_type', 'name']
        unique_together = [('user', 'name', 'entry_type')]

    def __str__(self):
        return f'{self.name} ({self.get_entry_type_display()})'


class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        unique_together = [('user', 'name')]

    def __str__(self):
        return self.name


class Entry(models.Model):
    EXPENSE = 'EXPENSE'
    INCOME = 'INCOME'
    ENTRY_TYPE_CHOICES = [(EXPENSE, 'Expense'), (INCOME, 'Income')]

    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'
    RECURRENCE_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
    )
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='entries',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='entries')
    date = models.DateField(default=date.today)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(
        max_length=10,
        choices=RECURRENCE_CHOICES,
        null=True,
        blank=True,
    )
    last_processed_at = models.DateField(
        null=True,
        blank=True,
        help_text='Last date process_recurring created an instance from this template.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'entries'

    def __str__(self):
        return f'{self.get_entry_type_display()} — {self.amount} on {self.date}'
