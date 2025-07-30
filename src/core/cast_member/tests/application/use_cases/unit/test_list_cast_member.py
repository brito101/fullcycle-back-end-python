import pytest
from uuid import uuid4

from src.core.cast_member.application.use_cases import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_list_cast_members_when_empty(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMember.Input()

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert output.data == []

    def test_list_cast_members_with_data(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member1 = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(name="Jane Doe", type=CastMemberType.DIRECTOR)
        repository.save(cast_member1)
        repository.save(cast_member2)
        
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMember.Input()

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert len(output.data) == 2
        assert cast_member1 in output.data
        assert cast_member2 in output.data

    def test_list_cast_members_returns_copy(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMember.Input()

        # Act
        output1 = use_case.execute(input_data)
        output2 = use_case.execute(input_data)

        # Assert
        assert output1.data is not output2.data  # Should be different objects
        assert output1.data == output2.data  # But same content 