from django.conf import settings
from django.db import models


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    category = models.ForeignKey(
        'core.Category',
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text='First day of the target month (YYYY-MM-01).')

    class Meta:
        unique_together = [('user', 'category', 'month')]
        ordering = ['-month', 'category__name']

    def __str__(self):
        return f'{self.category.name} budget — {self.month.strftime("%B %Y")}'
