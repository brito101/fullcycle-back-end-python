from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from src.core._shared.application.use_cases.list_use_case import (
    ListUseCase,
    ListRequest,
    ListResponse,
)

Entity = TypeVar("Entity")
Output = TypeVar("Output")
Repository = TypeVar("Repository")


class ListViewSet(Generic[Entity, Output, Repository], viewsets.ViewSet, ABC):

    @abstractmethod
    def _get_use_case(self) -> ListUseCase[Entity, Output]:
        pass

    @abstractmethod
    def _get_response_serializer(self, output: ListResponse[Output]):
        pass

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        use_case = self._get_use_case()
        output: ListResponse[Output] = use_case.execute(
            request=ListRequest(
                order_by=order_by,
                current_page=int(request.query_params.get("current_page", 1)),
            )
        )
        response_serializer = self._get_response_serializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        ) 