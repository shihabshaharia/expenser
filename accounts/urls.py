from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
