from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases.list_use_case import (
    ListUseCase,
    ListRequest,
    ListResponse,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class ListCategory(ListUseCase[Category, CategoryOutput]):
    def _to_output(self, entity: Category) -> CategoryOutput:
        return CategoryOutput(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )


# Type aliases for backward compatibility
ListCategoryRequest = ListRequest
ListCategoryResponse = ListResponse[CategoryOutput]
