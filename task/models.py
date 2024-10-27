from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(
        max_length=255, null=False,
        blank=False
    )
    description = models.TextField(
        null=True, blank=True
    )
    due_date = models.DateField(
        null=False, blank=False
    )
    created_at = models.DateField(
        auto_now=True
    )
    is_activate = models.BooleanField(
        default=True
    )
