import logging
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import ExtractedItem
from parsers.pipeline import run_full_scan
from core.utils.export_dashboard import build_multi_sheet_workbook, update_dashboard_snapshot

logger = logging.getLogger(__name__)
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate


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


def metrics_status_counts(request):
    """
    API: returns counts per status
    {
      "pending": 5,
      "approved": 10,
      "rejected": 1,
      "error": 2
    }
    """
    qs = (
        ExtractedItem.objects
        .values("status")
        .annotate(count=Count("id"))
    )
    data = {row["status"]: row["count"] for row in qs}
    # Ensure all keys exist
    for key in ["pending", "approved", "rejected", "error"]:
        data.setdefault(key, 0)
    return JsonResponse(data)


def metrics_source_counts(request):
    """
    API: returns counts per source_type
    {
      "form": 5,
      "email": 7,
      "invoice": 10
    }
    """
    qs = (
        ExtractedItem.objects
        .values("source_type")
        .annotate(count=Count("id"))
    )
    data = {row["source_type"]: row["count"] for row in qs}
    return JsonResponse(data)


def metrics_daily_counts(request):
    """
    API: returns daily counts per status for the last 14 days
    [
      {"date": "2025-11-01", "pending": 3, "approved": 1, "rejected": 0, "error": 0},
      ...
    ]
    """
    today = timezone.now().date()
    start_date = today - timezone.timedelta(days=13)

    qs = (
        ExtractedItem.objects
        .filter(created_at__date__gte=start_date)
        .annotate(day=TruncDate("created_at"))
        .values("day", "status")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Build a map: day -> {status -> count}
    days_map = {}
    for row in qs:
        day = row["day"]
        status = row["status"]
        count = row["count"]
        days_map.setdefault(day, {"pending": 0, "approved": 0, "rejected": 0, "error": 0})
        days_map[day][status] = count

    # Normalize to all days (even if 0)
    result = []
    for i in range(14):
        d = start_date + timezone.timedelta(days=i)
        base = {"date": d.isoformat(), "pending": 0, "approved": 0, "rejected": 0, "error": 0}
        if d in days_map:
            base.update(days_map[d])
        result.append(base)

    return JsonResponse(result, safe=False)
