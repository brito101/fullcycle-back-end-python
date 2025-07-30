from typing import List, Optional
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self):
        self.cast_members: List[CastMember] = []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> Optional[CastMember]:
        for cast_member in self.cast_members:
            if cast_member.id == id:
                return cast_member
        return None

    def list(self) -> List[CastMember]:
        return self.cast_members.copy()

    def update(self, cast_member: CastMember) -> None:
        for i, existing_cast_member in enumerate(self.cast_members):
            if existing_cast_member.id == cast_member.id:
                self.cast_members[i] = cast_member
                return
        raise ValueError(f"CastMember with id {cast_member.id} not found")

    def delete(self, id: UUID) -> None:
        for i, cast_member in enumerate(self.cast_members):
            if cast_member.id == id:
                del self.cast_members[i]
                return
        raise ValueError(f"CastMember with id {id} not found") 