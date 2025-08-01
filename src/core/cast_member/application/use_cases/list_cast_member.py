from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases.list_use_case import (
    ListUseCase,
    ListRequest,
    ListResponse,
)
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMember(ListUseCase[CastMember, CastMemberOutput]):
    def _to_output(self, entity: CastMember) -> CastMemberOutput:
        return CastMemberOutput(
            id=entity.id,
            name=entity.name,
            type=entity.type.value,
        )


# Type aliases for backward compatibility
ListCastMemberRequest = ListRequest
ListCastMemberResponse = ListResponse[CastMemberOutput] 