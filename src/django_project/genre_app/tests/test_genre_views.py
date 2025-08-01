from uuid import UUID, uuid4
from django.test import override_settings
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre

from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_romance: Genre,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url = "/api/genres/"
        response = APIClient().get(url)

        # TODO: Quando implementarmos ordenação, poderemos comparar expected_data
        # expected_data = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": "Romance",
        #             "is_active": True,
        #             "categories": [
        #                 str(category_documentary.id),
        #                 str(category_movie.id),
        #             ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": "Drama",
        #             "is_active": True,
        #             "categories": [],
        #         },
        #     ]
        # }

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]
        
        # Check that both genres are in the response (order doesn't matter due to sorting)
        genre_ids = [genre["id"] for genre in response.data["data"]]
        assert str(genre_romance.id) in genre_ids
        assert str(genre_drama.id) in genre_ids
        
        # Check meta information
        assert "meta" in response.data
        assert response.data["meta"]["current_page"] == 1
        assert response.data["meta"]["per_page"] == 2
        assert response.data["meta"]["total"] == 2
        
        # Find each genre by ID and verify its data
        for genre_data in response.data["data"]:
            if genre_data["id"] == str(genre_romance.id):
                assert genre_data["name"] == "Romance"
                assert genre_data["is_active"] is True
                assert set(genre_data["categories"]) == {
                    str(category_documentary.id),
                    str(category_movie.id),
                }
            elif genre_data["id"] == str(genre_drama.id):
                assert genre_data["name"] == "Drama"
                assert genre_data["is_active"] is True
                assert genre_data["categories"] == []


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "categories": [category_movie.id],
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_genre = genre_repository.get_by_id(response.data["id"])
        assert saved_genre == Genre(
            id=UUID(response.data["id"]),
            name="Romance",
            is_active=True,
            categories={category_movie.id},
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/genres/"
        data = {
            "name": "",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
    ) -> None:
        url = "/api/genres/"
        data = {
            "name": "Romance",
            "categories": [uuid4()],
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_pk_is_invalid_then_return_400(self) -> None:
        url = "/api/genres/invalid_uuid/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_genre_not_found_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_genre_found_then_delete_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(genre_romance.id) is None
