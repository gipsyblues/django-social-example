from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Action(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="actions")
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, models.CASCADE, blank=True, null=True)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey("target_ct", "target_id")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)
