from decimal import Decimal
from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoRequestSerializer,
    CreateVideoResponseSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateVideoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Convert serializer data to use case input
        input_data = serializer.validated_data
        use_case_input = CreateVideoWithoutMedia.Input(
            title=input_data["title"],
            description=input_data["description"],
            launch_year=input_data["year_launched"],
            opened=input_data["opened"],
            duration=input_data["duration"],
            rating=Rating[input_data["rating"]],
            categories=set(input_data["categories_id"]),
            genres=set(input_data["genres_id"]),
            cast_members=set(input_data["cast_members_id"]),
        )

        try:
            use_case = CreateVideoWithoutMedia(
                video_repository=DjangoORMVideoRepository(),
                category_repository=DjangoORMCategoryRepository(),
                genre_repository=DjangoORMGenreRepository(),
                cast_member_repository=DjangoORMCastMemberRepository(),
            )
            
            output = use_case.execute(request=use_case_input)

            return Response(
                status=HTTP_201_CREATED,
                data=CreateVideoResponseSerializer(output).data,
            )
        except (InvalidVideo, RelatedEntitiesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )