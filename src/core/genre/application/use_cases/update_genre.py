from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
    GenreNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    def __init__(
        self, repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool = True
        categories: set[UUID] = field(default_factory=set)

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]

    def execute(self, input: Input) -> Output:
        # Verificar se o gênero existe
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with id {input.id} not found")

        # Verificar se as categorias existem
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}"
            )

        try:
            # Criar novo gênero com os atributos atualizados
            updated_genre = Genre(
                id=input.id,
                name=input.name,
                is_active=input.is_active,
                categories=input.categories,
            )
        except ValueError as err:
            raise InvalidGenre(err)

        # Atualizar o gênero no repositório
        self.repository.update(updated_genre)
        
        return self.Output(
            id=updated_genre.id,
            name=updated_genre.name,
            is_active=updated_genre.is_active,
            categories=updated_genre.categories,
        ) 