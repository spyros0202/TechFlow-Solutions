# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("scan/", views.scan, name="scan"),
    path("item/<int:pk>/", views.detail, name="detail"),
    path("export/", views.export_items, name="export_items"),

    # Metrics API endpoints
    path("api/metrics/status/", views.metrics_status_counts, name="metrics_status"),
    path("api/metrics/source/", views.metrics_source_counts, name="metrics_source"),
    path("api/metrics/daily/", views.metrics_daily_counts, name="metrics_daily"),
]
