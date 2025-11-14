import logging
from io import BytesIO

import pandas as pd
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from core.models import ExtractedItem
from parsers.pipeline import run_full_scan
from core.utils.export_dashboard import build_multi_sheet_workbook, update_dashboard_snapshot

logger = logging.getLogger(__name__)


def dashboard(request):
    status_filter = request.GET.get("status", "pending")

    if status_filter == "all":
        items = ExtractedItem.objects.all().order_by("-created_at")
    else:
        items = ExtractedItem.objects.filter(status=status_filter).order_by("-created_at")

    return render(request, "dashboard.html", {
        "items": items,
        "current_status": status_filter,
    })


def scan(request):
    try:
        created, errors = run_full_scan()
        messages.info(request, f"Scan completed: {created} items, {errors} errors.")
    except Exception as e:
        logger.exception("Scan failed")
        messages.error(request, f"Scan failed: {e}")
    return redirect("dashboard")


def export_items(request):
    status_filter = request.GET.get("status", "all")

    try:
        buffer = build_multi_sheet_workbook(status_filter=status_filter)

        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response['Content-Disposition'] = f'attachment; filename=export_{status_filter}.xlsx'
        return response

    except Exception as e:
        logger.exception("Export failed")
        messages.error(request, f"Export failed: {e}")
        return redirect("dashboard")


def detail(request, pk):
    item = get_object_or_404(ExtractedItem, pk=pk)

    if request.method == "POST":
        updated_data = {
            k: v for k, v in request.POST.items()
            if k not in ["csrfmiddlewaretoken", "action"]
        }
        item.data = updated_data

        action = request.POST.get("action")

        if action == "approve":
            item.status = "approved"
            messages.success(request, "Item approved.")
        elif action == "reject":
            item.status = "rejected"
            messages.warning(request, "Item rejected.")
        else:  # save as pending
            item.status = "pending"
            messages.info(request, "Item saved as pending.")

        item.save()

        # Auto-update snapshot σε κάθε αλλαγή (auto-update integration)
        try:
            update_dashboard_snapshot()
        except Exception as e:
            logger.exception("Failed to update dashboard snapshot")
            # Δεν ρίχνουμε error στον χρήστη, απλά logging

        return redirect("dashboard")

    return render(request, "detail.html", {"item": item})
