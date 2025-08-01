import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class CastMember(models.Model):
    class CastMemberType(models.TextChoices):
        ACTOR = "ACTOR", _("Actor")
        DIRECTOR = "DIRECTOR", _("Director")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=CastMemberType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cast_members"
        verbose_name = _("Cast Member")
        verbose_name_plural = _("Cast Members")

    def __str__(self):
        return f"{self.name} ({self.type})" 