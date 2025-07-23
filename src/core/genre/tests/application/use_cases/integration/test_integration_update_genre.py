import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_with_existing_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        # Criar categorias
        cat_1 = Category(name="Category 1", description="Category 1 description")
        category_repository.save(cat_1)

        cat_2 = Category(name="Category 2", description="Category 2 description")
        category_repository.save(cat_2)

        cat_3 = Category(name="Category 3", description="Category 3 description")
        category_repository.save(cat_3)

        # Criar gênero inicial com 3 categorias
        genre = Genre(
            name="Drama",
            categories={cat_1.id, cat_2.id, cat_3.id},
            is_active=True,
        )
        genre_repository.save(genre)

        # Atualizar gênero com apenas 2 categorias e outros atributos
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        
        output = use_case.execute(
            UpdateGenre.Input(
                id=genre.id,
                name="Updated Drama",
                is_active=False,
                categories={cat_1.id, cat_2.id},
            )
        )

        # Verificar output
        assert output == UpdateGenre.Output(
            id=genre.id,
            name="Updated Drama",
            is_active=False,
            categories={cat_1.id, cat_2.id},
        )

        # Verificar se o gênero foi atualizado no repositório
        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Updated Drama"
        assert updated_genre.is_active == False
        assert updated_genre.categories == {cat_1.id, cat_2.id}

    def test_update_genre_that_does_not_exist(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        import uuid
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(GenreNotFound, match=f"Genre with id {non_existent_id} not found"):
            use_case.execute(
                UpdateGenre.Input(
                    id=non_existent_id,
                    name="Updated Genre",
                    is_active=True,
                    categories=set(),
                )
            )

    def test_update_genre_with_invalid_attributes(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        # Criar gênero
        genre = Genre(name="Drama", is_active=True)
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(
                UpdateGenre.Input(
                    id=genre.id,
                    name="",
                    is_active=True,
                    categories=set(),
                )
            )

    def test_update_genre_with_non_existent_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        # Criar gênero
        genre = Genre(name="Drama", is_active=True)
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        import uuid
        non_existent_category_id = uuid.uuid4()
        
        with pytest.raises(RelatedCategoriesNotFound, match="Categories with provided IDs not found: "):
            use_case.execute(
                UpdateGenre.Input(
                    id=genre.id,
                    name="Updated Genre",
                    is_active=True,
                    categories={non_existent_category_id},
                )
            )

    def test_update_genre_without_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        # Criar categorias
        cat_1 = Category(name="Category 1", description="Category 1 description")
        category_repository.save(cat_1)

        # Criar gênero com categoria
        genre = Genre(
            name="Drama",
            categories={cat_1.id},
            is_active=True,
        )
        genre_repository.save(genre)

        # Atualizar gênero sem categorias
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        
        output = use_case.execute(
            UpdateGenre.Input(
                id=genre.id,
                name="Updated Drama",
                is_active=False,
                categories=set(),
            )
        )

        # Verificar output
        assert output == UpdateGenre.Output(
            id=genre.id,
            name="Updated Drama",
            is_active=False,
            categories=set(),
        )

        # Verificar se o gênero foi atualizado no repositório
        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Updated Drama"
        assert updated_genre.is_active == False
        assert updated_genre.categories == set() 