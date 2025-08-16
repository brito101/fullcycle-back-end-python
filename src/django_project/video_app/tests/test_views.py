from decimal import Decimal
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

from src.django_project.category_app.models import Category
from src.django_project.cast_member_app.models import CastMember
from src.django_project.genre_app.models import Genre


class TestCreateVideoWithoutMedia:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name="Action",
            description="Action movies",
            is_active=True
        )

    @pytest.fixture
    def genre(self):
        return Genre.objects.create(
            name="Adventure",
            is_active=True
        )

    @pytest.fixture
    def cast_member(self):
        return CastMember.objects.create(
            name="John Doe",
            type="ACTOR"
        )

    @pytest.fixture
    def valid_video_data(self, category, genre, cast_member):
        return {
            "title": "Sample Video",
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(category.id)],
            "genres_id": [str(genre.id)],
            "cast_members_id": [str(cast_member.id)],
        }

    def test_create_video_without_media_success(
        self,
        api_client: APIClient,
        valid_video_data: dict,
    ):
        """Test successful video creation without media"""
        # Arrange
        url = reverse("video-list")

        # Act
        response = api_client.post(
            url,
            data=valid_video_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["id"] is not None

    def test_create_video_without_media_validation_errors(
        self,
        api_client: APIClient,
        category: Category,
        genre: Genre,
        cast_member: CastMember,
    ):
        """Test video creation with validation errors"""
        # Arrange
        url = reverse("video-list")
        invalid_data = {
            "title": "",  # Invalid: empty title
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(category.id)],
            "genres_id": [str(genre.id)],
            "cast_members_id": [str(cast_member.id)],
        }

        # Act
        response = api_client.post(
            url,
            data=invalid_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data  # Django REST Framework validation error

    def test_create_video_without_media_invalid_categories(
        self,
        api_client: APIClient,
        genre: Genre,
        cast_member: CastMember,
    ):
        """Test video creation with invalid category IDs"""
        # Arrange
        url = reverse("video-list")
        invalid_data = {
            "title": "Sample Video",
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(uuid4())],  # Invalid category ID
            "genres_id": [str(genre.id)],
            "cast_members_id": [str(cast_member.id)],
        }

        # Act
        response = api_client.post(
            url,
            data=invalid_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_without_media_invalid_genres(
        self,
        api_client: APIClient,
        category: Category,
        cast_member: CastMember,
    ):
        """Test video creation with invalid genre IDs"""
        # Arrange
        url = reverse("video-list")
        invalid_data = {
            "title": "Sample Video",
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(category.id)],
            "genres_id": [str(uuid4())],  # Invalid genre ID
            "cast_members_id": [str(cast_member.id)],
        }

        # Act
        response = api_client.post(
            url,
            data=invalid_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_without_media_invalid_cast_members(
        self,
        api_client: APIClient,
        category: Category,
        genre: Genre,
    ):
        """Test video creation with invalid cast member IDs"""
        # Arrange
        url = reverse("video-list")
        invalid_data = {
            "title": "Sample Video",
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(category.id)],
            "genres_id": [str(genre.id)],
            "cast_members_id": [str(uuid4())],  # Invalid cast member ID
        }

        # Act
        response = api_client.post(
            url,
            data=invalid_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_without_media_multiple_validation_errors(
        self,
        api_client: APIClient,
    ):
        """Test video creation with multiple validation errors"""
        # Arrange
        url = reverse("video-list")
        invalid_data = {
            "title": "Sample Video",
            "description": "A test video description",
            "year_launched": 2022,
            "opened": True,
            "duration": "120.5",
            "rating": "AGE_12",
            "categories_id": [str(uuid4())],  # Invalid category ID
            "genres_id": [str(uuid4())],      # Invalid genre ID
            "cast_members_id": [str(uuid4())], # Invalid cast member ID
        }

        # Act
        response = api_client.post(
            url,
            data=invalid_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
