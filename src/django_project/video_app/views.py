from decimal import Decimal
from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
from rest_framework.decorators import action

from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound, VideoNotFound
from src.core.video.domain.value_objects import Rating
from src.core._shared.infra.storage.abstract_storage import AbstractStorage
from src.core._shared.events.message_bus import MessageBus
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

    @action(detail=True, methods=['post'], url_path='upload-media')
    def upload_media(self, request: Request, pk: str) -> Response:
        print(f"Debug: Iniciando upload para video ID: {pk}")
        print(f"Debug: Request FILES: {request.FILES}")
        print(f"Debug: Request data: {request.data}")
        
        try:
            video_id = UUID(pk)
        except ValueError:
            print(f"Debug: ID inválido: {pk}")
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": "Invalid video ID"},
            )

        # Get file from request
        if 'file' not in request.FILES:
            print(f"Debug: Nenhum arquivo encontrado em request.FILES")
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": "No file provided"},
            )

        file = request.FILES['file']
        file_name = file.name
        content = file.read()
        content_type = file.content_type
        
        print(f"Debug: Arquivo recebido - Nome: {file_name}, Tipo: {content_type}, Tamanho: {len(content)}")

        try:
            print(f"Debug: Criando use case UploadVideo")
            use_case = UploadVideo(
                repository=DjangoORMVideoRepository(),
                storage_service=request.storage_service if hasattr(request, 'storage_service') else None,
                message_bus=request.message_bus if hasattr(request, 'message_bus') else None,
            )
            
            print(f"Debug: Executando use case")
            use_case.execute(
                UploadVideo.Input(
                    video_id=video_id,
                    file_name=file_name,
                    content=content,
                    content_type=content_type,
                )
            )
            
            print(f"Debug: Upload concluído com sucesso")
            return Response(
                status=HTTP_200_OK,
                data={"message": "Media uploaded successfully"},
            )
        except VideoNotFound as e:
            print(f"Debug: Video não encontrado: {e}")
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )
        except Exception as e:
            print(f"Debug: Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": f"Upload failed: {str(e)}"},
            )
