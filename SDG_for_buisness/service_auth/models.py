import secrets

from django.db import models


class ServiceClient(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    api_key = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    scopes = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "service_clients"
        ordering = ["name"]

    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(32)

        super().save(*args, **kwargs)

    def has_scope(self, scope):
        return scope in self.scopes

    def __str__(self):
        return self.name