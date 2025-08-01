from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases.list_use_case import (
    ListUseCase,
    ListRequest,
    ListResponse,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: set[UUID]
    is_active: bool


class ListGenre(ListUseCase[Genre, GenreOutput]):
    def _to_output(self, entity: Genre) -> GenreOutput:
        return GenreOutput(
            id=entity.id,
            name=entity.name,
            categories=entity.categories,
            is_active=entity.is_active,
        )


# Type aliases for backward compatibility
ListGenreRequest = ListRequest
ListGenreResponse = ListResponse[GenreOutput]
