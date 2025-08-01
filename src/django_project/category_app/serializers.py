from rest_framework import serializers

from src.core._shared.infra.django.serializers import (
    ListResponseSerializer,
    ListOutputMetaSerializer,
)


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(ListResponseSerializer):
    def _get_item_serializer(self) -> serializers.Serializer:
        return CategoryResponseSerializer()


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=False
    )
    is_active = serializers.BooleanField(default=True)


class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(
        required=True, allow_blank=True, allow_null=False
    )
    is_active = serializers.BooleanField(required=True)


class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
