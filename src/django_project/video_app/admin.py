from django.contrib import admin

from .models import Video, ImageMedia, AudioVideoMedia


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "launch_year", "rating", "opened", "published"]
    list_filter = ["rating", "opened", "published", "launch_year"]
    search_fields = ["title", "description"]
    readonly_fields = ["id"]


@admin.register(ImageMedia)
class ImageMediaAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "checksum", "raw_location"]
    search_fields = ["name", "checksum"]
    readonly_fields = ["id"]


@admin.register(AudioVideoMedia)
class AudioVideoMediaAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "checksum", "status", "raw_location", "encoded_location"]
    list_filter = ["status"]
    search_fields = ["name", "checksum"]
    readonly_fields = ["id"]