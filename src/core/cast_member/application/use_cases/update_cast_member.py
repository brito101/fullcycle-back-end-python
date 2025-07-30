from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> Output:
        # Verificar se o cast member existe
        existing_cast_member = self.repository.get_by_id(input.id)
        if not existing_cast_member:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")

        try:
            # Criar novo cast member com os atributos atualizados
            updated_cast_member = CastMember(
                id=input.id,
                name=input.name,
                type=input.type,
            )
        except ValueError as err:
            raise InvalidCastMember(str(err))

        # Atualizar o cast member no repositório
        self.repository.update(updated_cast_member)
        
        return self.Output(
            id=updated_cast_member.id,
            name=updated_cast_member.name,
            type=updated_cast_member.type,
        ) 