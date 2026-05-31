from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('entries/', include('core.urls')),
    path('budgets/', include('budgets.urls')),
    path('reports/', include('reports.urls')),
    path('', include('core.dashboard_urls')),
]
