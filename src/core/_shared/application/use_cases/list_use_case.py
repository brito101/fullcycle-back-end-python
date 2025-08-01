from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Protocol

from src import config


@dataclass
class ListRequest:
    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0


T = TypeVar("T")
Entity = TypeVar("Entity")
Output = TypeVar("Output")


class Repository(Protocol[Entity]):
    def list(self) -> list[Entity]:
        ...


class ListUseCase(Generic[Entity, Output], ABC):
    def __init__(self, repository: Repository[Entity]) -> None:
        self.repository = repository

    @abstractmethod
    def _to_output(self, entity: Entity) -> Output:
        pass

    def execute(self, request: ListRequest) -> "ListResponse[Output]":
        entities = self.repository.list()
        ordered_entities = sorted(
            entities,
            key=lambda entity: getattr(entity, request.order_by),
        )
        page_offset = (request.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        entities_page = ordered_entities[
            page_offset : page_offset + config.DEFAULT_PAGINATION_SIZE
        ]

        return ListResponse(
            data=sorted(
                [self._to_output(entity) for entity in entities_page],
                key=lambda output: getattr(output, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(entities),
            ),
        )


@dataclass
class ListResponse(Generic[Output]):
    data: list[Output] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta) 