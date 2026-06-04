from django.contrib import admin
from .models import Budget

//he

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'month']
    list_filter = ['month', 'category']
    search_fields = ['category__name', 'user__username']
    raw_id_fields = ['user', 'category']
