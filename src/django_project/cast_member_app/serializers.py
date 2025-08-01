from rest_framework import serializers

from src.core._shared.infra.django.serializers import (
    ListResponseSerializer,
    ListOutputMetaSerializer,
)


class CastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)


class ListCastMemberOutputSerializer(ListResponseSerializer):
    def _get_item_serializer(self) -> serializers.Serializer:
        return CastMemberOutputSerializer()


class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)


class CreateCastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    type = serializers.CharField(required=True) 