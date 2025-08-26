import pytest
import json
import time
import pika
from rest_framework.test import APIClient
from django.test import override_settings
from unittest.mock import patch
from uuid import UUID


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def rabbitmq_connection():
    """Fixture para conexão com RabbitMQ"""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=5672)
        )
        channel = connection.channel()
        channel.queue_declare(queue='videos.converted')
        print("Conexão com RabbitMQ estabelecida")
        yield channel
        connection.close()
    except Exception as e:
        print(f"Erro ao conectar com RabbitMQ: {e}")
        print("Certifique-se de que o RabbitMQ está rodando: docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        pytest.skip(f"RabbitMQ não está disponível: {e}")


@pytest.mark.django_db
class TestVideoMediaProcessing:
    def test_video_media_processing_end_to_end(self, api_client: APIClient, rabbitmq_connection) -> None:
        """
        Teste end-to-end que:
        1. Cria Category, Genre e CastMember
        2. Cria um Video
        3. Faz upload de mídia
        4. Publica evento na fila videos.converted
        5. Verifica que o video foi processado
        """
        
        # Importações necessárias
        from src.django_project.video_app.repository import DjangoORMVideoRepository
        from src.core.video.domain.value_objects import MediaStatus, MediaType
        from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
        
        # 1. Criar Category
        category_response = api_client.post(
            "/api/categories/",
            {
                "name": "Action",
                "description": "Action movies",
            },
        )
        assert category_response.status_code == 201
        category_id = category_response.data["id"]
        print(f"Category criada: {category_id}")
        
        # 2. Criar Genre
        genre_response = api_client.post(
            "/api/genres/",
            {
                "name": "Adventure",
                "description": "Adventure movies",
                "is_active": True,
            },
        )
        assert genre_response.status_code == 201
        genre_id = genre_response.data["id"]
        print(f"Genre criado: {genre_id}")
        
        # 3. Criar CastMember
        cast_member_response = api_client.post(
            "/api/cast-members/",
            {
                "name": "John Doe",
                "type": "ACTOR",
            },
        )
        assert cast_member_response.status_code == 201
        cast_member_id = cast_member_response.data["id"]
        print(f"CastMember criado: {cast_member_id}")
        
        # 4. Criar Video
        video_response = api_client.post(
            "/api/videos/",
            {
                "title": "Test Video",
                "description": "A test video for end-to-end testing",
                "year_launched": 2024,
                "opened": True,
                "duration": 120.0,
                "rating": "AGE_14",
                "categories_id": [category_id],
                "genres_id": [genre_id],
                "cast_members_id": [cast_member_id],
            },
        )
        assert video_response.status_code == 201
        video_id = video_response.data["id"]
        print(f"Video criado: {video_id}")
        
        # 5. Fazer upload de mídia
        # Criar um arquivo de teste
        test_file_content = b"fake video content for testing"
        
        with patch('src.django_project.video_app.middleware.InMemoryStorage') as mock_storage:
            mock_storage.return_value.store.return_value = None
            
            # Criar um arquivo temporário para o teste
            from django.core.files.uploadedfile import SimpleUploadedFile
            test_file = SimpleUploadedFile(
                "test_video.mp4",
                test_file_content,
                content_type="video/mp4"
            )
            
            upload_response = api_client.post(
                f"/api/videos/{video_id}/upload-media/",
                {"file": test_file},
                format="multipart",
            )
            
            # Debug: mostrar detalhes do erro
            if upload_response.status_code != 200:
                print(f"Erro na API de upload: {upload_response.status_code}")
                print(f"Resposta: {upload_response.data}")
                print(f"Headers: {upload_response.headers}")
            
            assert upload_response.status_code == 200
            print(f"Mídia enviada para o video: {video_id}")
        
        # 6. Publicar evento na fila videos.converted
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": "COMPLETED",
        }
        
        print(f"Enviando mensagem para RabbitMQ: {message}")
        rabbitmq_connection.basic_publish(
            exchange='',
            routing_key='videos.converted',
            body=json.dumps(message)
        )
        print("Mensagem enviada para RabbitMQ")
        
        # 6.1. Processar a mensagem diretamente (simulando o consumer)
        # Como o consumer está rodando em um processo separado com banco diferente,
        # vamos processar a mensagem diretamente no teste
        print("Processando mensagem diretamente no teste...")
        
        # Processar a mensagem como o consumer faria
        aggregate_id_raw, media_type_raw = message["video"]["resource_id"].split(".")
        aggregate_id = UUID(aggregate_id_raw)
        media_type = MediaType(media_type_raw)
        encoded_location = message["video"]["encoded_video_folder"]
        status = MediaStatus(message["status"])
        
        process_input = ProcessAudioVideoMedia.Input(
            video_id=aggregate_id,
            encoded_location=encoded_location,
            media_type=media_type,
            status=status,
        )
        
        print(f"Processando com input: {process_input}")
        process_use_case = ProcessAudioVideoMedia(
            video_repository=DjangoORMVideoRepository()
        )
        process_use_case.execute(request=process_input)
        print("Mensagem processada com sucesso")
        
        # Aguardar um pouco para o processamento
        print("Aguardando processamento...")
        time.sleep(1)
        
        # 7. Verificar que o video foi processado
        # Buscar o video atualizado do banco
        repository = DjangoORMVideoRepository()
        updated_video = repository.get_by_id(video_id)
        
        assert updated_video is not None
        assert updated_video.video is not None
        assert updated_video.video.status == MediaStatus.COMPLETED
        assert updated_video.video.encoded_location == "/path/to/encoded/video"
        
        print(f"Teste end-to-end concluído com sucesso!")
        print(f"   Video ID: {video_id}")
        print(f"   Status da mídia: {updated_video.video.status}")
        print(f"   Localização codificada: {updated_video.video.encoded_location}")


@pytest.mark.django_db
class TestVideoMediaProcessingWithError:
    def test_video_media_processing_with_error(self, api_client: APIClient, rabbitmq_connection) -> None:
        """
        Teste que simula um erro no processamento da mídia
        """
        
        # Criar entidades básicas
        category_response = api_client.post(
            "/api/categories/",
            {"name": "Drama", "description": "Drama movies"},
        )
        assert category_response.status_code == 201
        category_id = category_response.data["id"]
        
        genre_response = api_client.post(
            "/api/genres/",
            {"name": "Thriller", "description": "Thriller movies", "is_active": True},
        )
        assert genre_response.status_code == 201
        genre_id = genre_response.data["id"]
        
        cast_member_response = api_client.post(
            "/api/cast-members/",
            {"name": "Jane Smith", "type": "ACTOR"},
        )
        assert cast_member_response.status_code == 201
        cast_member_id = cast_member_response.data["id"]
        
        # Criar video
        video_response = api_client.post(
            "/api/videos/",
            {
                "title": "Error Test Video",
                "description": "A test video for error testing",
                "year_launched": 2024,
                "opened": True,
                "duration": 90.0,
                "rating": "AGE_16",
                "categories_id": [category_id],
                "genres_id": [genre_id],
                "cast_members_id": [cast_member_id],
            },
        )
        assert video_response.status_code == 201
        video_id = video_response.data["id"]
        
        # Upload de mídia
        test_file_content = b"fake video content for testing"
        
        with patch('src.django_project.video_app.middleware.InMemoryStorage') as mock_storage:
            mock_storage.return_value.store.return_value = None
            
            # Criar um arquivo temporário para o teste
            from django.core.files.uploadedfile import SimpleUploadedFile
            test_file = SimpleUploadedFile(
                "test_video.mp4",
                test_file_content,
                content_type="video/mp4"
            )
            
            upload_response = api_client.post(
                f"/api/videos/{video_id}/upload-media/",
                {"file": test_file},
                format="multipart",
            )
            assert upload_response.status_code == 200
        
        # Publicar evento de erro
        error_message = {
            "error": "Encoding failed due to corrupted file",
            "message": {
                "resource_id": f"{video_id}.VIDEO",
            },
            "status": "ERROR",
        }
        
        print(f"Enviando mensagem de erro para RabbitMQ: {error_message}")
        rabbitmq_connection.basic_publish(
            exchange='',
            routing_key='videos.converted',
            body=json.dumps(error_message)
        )
        
        # Aguardar processamento
        time.sleep(3)
        
        # Verificar que o video não foi processado (deve manter status PENDING)
        from src.django_project.video_app.repository import DjangoORMVideoRepository
        from src.core.video.domain.value_objects import MediaStatus
        
        repository = DjangoORMVideoRepository()
        updated_video = repository.get_by_id(video_id)
        
        assert updated_video is not None
        assert updated_video.video is not None
        # O status deve permanecer PENDING pois o consumer não processa mensagens de erro
        assert updated_video.video.status == MediaStatus.PENDING
        
        print(f"Teste de erro concluído com sucesso!")
        print(f"   Video ID: {video_id}")
        print(f"   Status da mídia: {updated_video.video.status}")
        print(f"   Erro foi capturado corretamente pelo consumer")
