from django.contrib import admin
from .models import Category, Entry, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'entry_type', 'user']
    list_filter = ['entry_type']
    search_fields = ['name', 'user__username']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name', 'user__username']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'entry_type', 'amount', 'category', 'date', 'is_recurring', 'created_at']
    list_filter = ['entry_type', 'category', 'is_recurring', 'date']
    search_fields = ['description', 'tags__name', 'user__username']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'last_processed_at']
    filter_horizontal = ['tags']
    raw_id_fields = ['user', 'category']
