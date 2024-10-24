from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False
    )
    description = models.TextField(
        null=False, blank=True
    )
    product_id = models.CharField(
        max_length=20, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    product_in_date = models.DateField(
        auto_now=True
    )
