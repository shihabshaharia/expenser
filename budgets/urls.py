from django.urls import path
from . import views

urlpatterns = [
    path('', views.BudgetListView.as_view(), name='budget_list'),
    path('add/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='budget_update'),
    path('<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget_delete'),
]
