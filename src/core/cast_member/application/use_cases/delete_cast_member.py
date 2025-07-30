from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        # Verificar se o cast member existe
        cast_member = self.repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")

        # Deletar o cast member
        self.repository.delete(input.id) 