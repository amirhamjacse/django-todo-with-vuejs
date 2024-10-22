from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(
        max_length=200, null=True, blank=False
    )
    description = models.TextField(
        blank=True, null=True
    )
    completed = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    due_date = models.DateTimeField(
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
