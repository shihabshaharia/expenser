from django.urls import path
from . import views

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('add/', views.EntryCreateView.as_view(), name='entry_create'),
    path('<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
