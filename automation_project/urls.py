from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Όλο το UI (dashboard, detail, scan) το δίνουμε στο dashboard app
    path("", include("dashboard.urls")),
]
