from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, cast_member: CastMember) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[CastMember]:
        pass

    @abstractmethod
    def list(self) -> List[CastMember]:
        pass

    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass 