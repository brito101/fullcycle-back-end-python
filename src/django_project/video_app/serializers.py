from rest_framework import serializers

from src.core._shared.infra.django.serializers import (
    ListResponseSerializer,
    ListOutputMetaSerializer,
)


class VideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = serializers.CharField(max_length=10)
    opened = serializers.BooleanField()
    published = serializers.BooleanField()


class ListVideoOutputSerializer(ListResponseSerializer):
    def _get_item_serializer(self) -> serializers.Serializer:
        return VideoOutputSerializer()


class CreateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    year_launched = serializers.IntegerField()
    opened = serializers.BooleanField(default=False)
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = serializers.CharField(max_length=10)
    categories_id = serializers.ListField(child=serializers.UUIDField())
    genres_id = serializers.ListField(child=serializers.UUIDField())
    cast_members_id = serializers.ListField(child=serializers.UUIDField())


class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    year_launched = serializers.IntegerField(required=True)
    duration = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    rating = serializers.CharField(max_length=10, required=True)
    opened = serializers.BooleanField(required=True)
    categories_id = serializers.ListField(child=serializers.UUIDField(), required=True)
    genres_id = serializers.ListField(child=serializers.UUIDField(), required=True)
    cast_members_id = serializers.ListField(child=serializers.UUIDField(), required=True)


class DeleteVideoRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
