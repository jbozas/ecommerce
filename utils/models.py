from django.db import models


class TimeStampedModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, db_index=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
