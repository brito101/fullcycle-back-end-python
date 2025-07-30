from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class CastMemberType(str, Enum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass(frozen=True)
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        
        if not isinstance(self.type, CastMemberType):
            raise ValueError("Type must be a valid CastMemberType") 