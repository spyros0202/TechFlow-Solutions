import logging
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import ExtractedItem
from parsers.pipeline import run_full_scan
from core.utils.export_dashboard import build_multi_sheet_workbook, update_dashboard_snapshot

# Initialize module-level logger
logger = logging.getLogger(__name__)

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate


def dashboard(request):
    """
    Render the main dashboard page.
    Allows filtering items by status (pending, approved, rejected, error, all).
    """
    # Read the status filter from query params (default: 'pending')
    status_filter = request.GET.get("status", "pending")

    # Apply filtering logic
    if status_filter == "all":
        items = ExtractedItem.objects.all().order_by("-created_at")
    else:
        items = ExtractedItem.objects.filter(status=status_filter).order_by("-created_at")

    # Return dashboard template with context
    return render(request, "dashboard.html", {
        "items": items,
        "current_status": status_filter,
    })


def scan(request):
    """
    Trigger the full data extraction pipeline.
    Reads all dummy_data, extracts fields, populates DB.
    Includes exception handling and user feedback.
    """
    try:
        # Run extraction pipeline for forms/emails/invoices
        created, errors = run_full_scan()
        messages.info(request, f"Scan completed: {created} items, {errors} errors.")
    except Exception as e:
        # Log and show error to the UI
        logger.exception("Scan failed")
        messages.error(request, f"Scan failed: {e}")
    return redirect("dashboard")


def export_items(request):
    """
    Export the DB contents into a multi-sheet XLSX file.
    Includes error handling and returns the file as a download.
    """
    status_filter = request.GET.get("status", "all")

    try:
        # Build the Excel file completely in memory
        buffer = build_multi_sheet_workbook(status_filter=status_filter)

        # Prepare streaming response
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response['Content-Disposition'] = f'attachment; filename=export_{status_filter}.xlsx'
        return response

    except Exception as e:
        # If export fails: log and notify user
        logger.exception("Export failed")
        messages.error(request, f"Export failed: {e}")
        return redirect("dashboard")


def detail(request, pk):
    """
    Detail page for reviewing/modifying a single ExtractedItem.
    Supports:
      - Approve
      - Reject
      - Save as pending
    Performs auto-update of the Excel dashboard on every modification.
    """
    # Load requested object or 404
    item = get_object_or_404(ExtractedItem, pk=pk)

    if request.method == "POST":
        # Extract all POST form fields except control variables
        updated_data = {
            k: v for k, v in request.POST.items()
            if k not in ["csrfmiddlewaretoken", "action"]
        }
        item.data = updated_data

        # Determine user action
        action = request.POST.get("action")

        if action == "approve":
            item.status = "approved"
            messages.success(request, "Item approved.")
        elif action == "reject":
            item.status = "rejected"
            messages.warning(request, "Item rejected.")
        else:
            # Save without approving/rejecting → stays pending
            item.status = "pending"
            messages.info(request, "Item saved as pending.")

        # Save changes
        item.save()

        # Auto-update Excel snapshot — non-blocking, silent on failure
        try:
            update_dashboard_snapshot()
        except Exception as e:
            logger.exception("Failed to update dashboard snapshot")
            # No user-facing error → we keep UX clean

        return redirect("dashboard")

    # Render detail page (GET)
    return render(request, "detail.html", {"item": item})


def metrics_status_counts(request):
    """
    API endpoint:
    Returns JSON with counts per status.
    Consumed by Chart.js on the dashboard for real-time analytics.
    Example response:
    {
        "pending": 5,
        "approved": 10,
        "rejected": 1,
        "error": 2
    }
    """
    # Aggregate DB entries by status
    qs = (
        ExtractedItem.objects
        .values("status")
        .annotate(count=Count("id"))
    )

    # Convert queryset into simple dict
    data = {row["status"]: row["count"] for row in qs}

    # Ensure missing statuses return 0
    for key in ["pending", "approved", "rejected", "error"]:
        data.setdefault(key, 0)

    return JsonResponse(data)


def metrics_source_counts(request):
    """
    API endpoint:
    Returns JSON with counts per source_type.
    Example:
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
    API endpoint:
    Returns daily counts per status for the last 14 days.
    Used to feed the "Items per Day" analytics chart.
    Example:
    [
      {"date": "2025-11-01", "pending": 3, "approved": 1, "rejected": 0, "error": 0},
      ...
    ]
    """
    today = timezone.now().date()
    start_date = today - timezone.timedelta(days=13)

    # Query: group by date + status
    qs = (
        ExtractedItem.objects
        .filter(created_at__date__gte=start_date)
        .annotate(day=TruncDate("created_at"))
        .values("day", "status")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Build dictionary: day -> {status -> count}
    days_map = {}
    for row in qs:
        day = row["day"]
        status = row["status"]
        count = row["count"]

        # Ensure structure exists
        days_map.setdefault(day, {"pending": 0, "approved": 0, "rejected": 0, "error": 0})
        days_map[day][status] = count

    # Normalize all 14 days (even if no data)
    result = []
    for i in range(14):
        d = start_date + timezone.timedelta(days=i)
        base = {"date": d.isoformat(), "pending": 0, "approved": 0, "rejected": 0, "error": 0}

        # If we have data for that day, merge it
        if d in days_map:
            base.update(days_map[d])

        result.append(base)

    # Return list of dicts
    return JsonResponse(result, safe=False)
