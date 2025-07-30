from dataclasses import dataclass
from typing import List

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: List[CastMember]

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()
        return self.Output(data=cast_members) 