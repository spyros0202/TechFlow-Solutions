from django.db import models
from django.utils import timezone

class ExtractedItem(models.Model):
    SOURCE_TYPES = (
        ("form", "Form"),
        ("email", "Email"),
        ("invoice", "Invoice"),
    )

    STATUS_TYPES = (
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("error", "Error"),
    )

    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    source_file = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default="pending")

    raw_content = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def is_editable(self):
        # Extracted approved/rejected items cannot be edited
        return self.status in ["pending", "error"]

    def __str__(self):
        return f"{self.id} - {self.source_file} ({self.source_type})"
