from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from rest_framework import serializers

Output = TypeVar("Output")


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListResponseSerializer(serializers.Serializer):

    def _get_item_serializer(self) -> serializers.Serializer:
        raise NotImplementedError

    def to_representation(self, instance):
        item_serializer = self._get_item_serializer()

        return {
            "data": [item_serializer.to_representation(item) for item in instance.data],
            "meta": {
                "current_page": instance.meta.current_page,
                "per_page": instance.meta.per_page,
                "total": instance.meta.total,
            },
        }
