from rest_framework import serializers

from src.core._shared.infra.django.serializers import (
    ListResponseSerializer,
    ListOutputMetaSerializer,
)


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreOutputSerializer(ListResponseSerializer):
    def _get_item_serializer(self) -> serializers.Serializer:
        return GenreOutputSerializer()


class SetField(serializers.ListField):
    # Outras alternativas:
    # Na view, converter para Set manualmente
    # Utilizar o SerializerMethodField
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField(), required=False)


class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)
    categories = SetField(
        child=serializers.UUIDField(), required=True, allow_empty=True
    )
