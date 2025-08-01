from django.contrib import admin
from .models import CastMember


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("name",) 