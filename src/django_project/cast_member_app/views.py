from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from src.core.cast_member.application.use_cases import (
    CreateCastMember,
    DeleteCastMember,
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
)
from src.core._shared.infra.django.views import ListViewSet
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    ListCastMemberOutputSerializer,
    CreateCastMemberInputSerializer,
    DeleteCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    UpdateCastMemberInputSerializer,
)


class CastMemberViewSet(ListViewSet, viewsets.ViewSet):
    def _get_use_case(self) -> ListCastMember:
        return ListCastMember(repository=DjangoORMCastMemberRepository())

    def _get_response_serializer(self, output: ListCastMemberResponse):
        return ListCastMemberOutputSerializer(output)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Convert string to enum
        validated_data = serializer.validated_data.copy()
        validated_data["type"] = CastMemberType(validated_data["type"])

        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            output = use_case.execute(CreateCastMember.Input(**validated_data))
        except InvalidCastMember as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberOutputSerializer(output).data,
        )

    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteCastMemberInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        input = DeleteCastMember.Input(**request_data.validated_data)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"CastMember with id {pk} not found"},
            )

        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateCastMemberInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        
        # Convert string to enum
        validated_data = serializer.validated_data.copy()
        validated_data["type"] = CastMemberType(validated_data["type"])
        
        input = UpdateCastMember.Input(**validated_data)

        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"CastMember with id {pk} not found"},
            )
        except InvalidCastMember as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(status=HTTP_204_NO_CONTENT) 