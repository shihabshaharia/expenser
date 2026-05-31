from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportView.as_view(), name='report'),
    path('export/', views.ExportCSVView.as_view(), name='report_export'),
]
