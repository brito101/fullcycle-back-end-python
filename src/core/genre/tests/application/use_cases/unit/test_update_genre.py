import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
    GenreNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


@pytest.fixture
def existing_genre() -> Genre:
    return Genre(
        id=uuid.uuid4(),
        name="Drama",
        is_active=True,
        categories={uuid.uuid4(), uuid.uuid4()},
    )


@pytest.fixture
def mock_genre_repository_with_genre(existing_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.get_by_id.return_value = existing_genre
    return repository


@pytest.fixture
def mock_genre_repository_without_genre() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.get_by_id.return_value = None
    return repository


class TestUpdateGenre:
    def test_when_genre_does_not_exist_then_raise_genre_not_found(
        self,
        mock_genre_repository_without_genre,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_without_genre,
            category_repository=mock_category_repository_with_categories,
        )

        genre_id = uuid.uuid4()
        with pytest.raises(GenreNotFound, match=f"Genre with id {genre_id} not found"):
            use_case.execute(
                UpdateGenre.Input(
                    id=genre_id,
                    name="Updated Genre",
                    is_active=True,
                    categories=set(),
                )
            )

    def test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        existing_genre,
        mock_genre_repository_with_genre,
        mock_empty_category_repository,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_with_genre,
            category_repository=mock_empty_category_repository,
        )

        with pytest.raises(
            RelatedCategoriesNotFound, match="Categories with provided IDs not found: "
        ) as exc:
            category_id = uuid.uuid4()
            use_case.execute(
                UpdateGenre.Input(
                    id=existing_genre.id,
                    name="Updated Genre",
                    categories={category_id},
                )
            )

        assert str(category_id) in str(exc.value)

    def test_when_updated_genre_is_invalid_then_raise_invalid_genre(
        self,
        existing_genre,
        mock_genre_repository_with_genre,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_with_genre,
            category_repository=mock_category_repository_with_categories,
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(
                UpdateGenre.Input(
                    id=existing_genre.id,
                    name="",
                    is_active=True,
                    categories=set(),
                )
            )

    def test_when_updated_genre_is_valid_and_categories_exist_then_update_genre(
        self,
        existing_genre,
        movie_category,
        documentary_category,
        mock_genre_repository_with_genre,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_with_genre,
            category_repository=mock_category_repository_with_categories,
        )

        output = use_case.execute(
            UpdateGenre.Input(
                id=existing_genre.id,
                name="Updated Genre",
                is_active=False,
                categories={movie_category.id, documentary_category.id},
            )
        )

        assert output == UpdateGenre.Output(
            id=existing_genre.id,
            name="Updated Genre",
            is_active=False,
            categories={movie_category.id, documentary_category.id},
        )
        
        # Verificar se o método update foi chamado com o gênero atualizado
        mock_genre_repository_with_genre.update.assert_called_once()
        updated_genre = mock_genre_repository_with_genre.update.call_args[0][0]
        assert updated_genre.id == existing_genre.id
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.is_active == False
        assert updated_genre.categories == {movie_category.id, documentary_category.id}

    def test_update_genre_without_categories(
        self,
        existing_genre,
        mock_genre_repository_with_genre,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_with_genre,
            category_repository=mock_category_repository_with_categories,
        )

        output = use_case.execute(
            UpdateGenre.Input(
                id=existing_genre.id,
                name="Updated Genre",
                is_active=True,
            )
        )

        assert output == UpdateGenre.Output(
            id=existing_genre.id,
            name="Updated Genre",
            is_active=True,
            categories=set(),
        )

    def test_update_genre_replacing_all_categories(
        self,
        existing_genre,
        movie_category,
        mock_genre_repository_with_genre,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository_with_genre,
            category_repository=mock_category_repository_with_categories,
        )

        # O gênero original tinha 2 categorias, vamos substituir por apenas 1
        output = use_case.execute(
            UpdateGenre.Input(
                id=existing_genre.id,
                name="Updated Genre",
                is_active=True,
                categories={movie_category.id},
            )
        )

        assert output == UpdateGenre.Output(
            id=existing_genre.id,
            name="Updated Genre",
            is_active=True,
            categories={movie_category.id},
        )
        
        # Verificar se o método update foi chamado com apenas 1 categoria
        mock_genre_repository_with_genre.update.assert_called_once()
        updated_genre = mock_genre_repository_with_genre.update.call_args[0][0]
        assert len(updated_genre.categories) == 1
        assert movie_category.id in updated_genre.categories 