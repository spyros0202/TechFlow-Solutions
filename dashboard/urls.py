from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),          # homepage
    path("scan/", views.scan, name="scan"),              # run_full_scan()
    path("item/<int:pk>/", views.detail, name="detail"), # review/edit/approve/reject
    path("export/", views.export_items, name="export_items"),
]
