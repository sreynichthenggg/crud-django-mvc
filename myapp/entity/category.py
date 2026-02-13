"""Django ORM models for this bounded context."""

from django.db import models

from ..base import BaseEntity


class Category(BaseEntity):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255, blank=True)
    user_id = models.CharField(max_length=64, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "categories"

    def __str__(self) -> str:
        return f"{self.name}"
